"""ViSP science calibration task."""
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.time import TimeDelta
from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_processing_math.arithmetic import divide_arrays_by_array
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from dkist_processing_pac.optics.telescope import get_TM_db_location
from dkist_processing_pac.optics.telescope import Telescope

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess
from dkist_processing_visp.tasks.mixin.corrections import CorrectionsMixin
from dkist_processing_visp.tasks.mixin.input_frame_loaders import InputFrameLoadersMixin
from dkist_processing_visp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_visp.tasks.visp_base import VispTaskBase


@dataclass
class CalibrationCollection:
    """Dataclass to hold all calibration objects and allow for easy, property-based access."""

    dark: dict
    solar_gain: dict
    angle: dict
    state_offset: dict
    spec_shift: dict
    demod_matrices: Optional[dict]


class ScienceCalibration(
    VispTaskBase,
    IntermediateFrameHelpersMixin,
    InputFrameLoadersMixin,
    CorrectionsMixin,
    QualityMixin,
):
    """
    Task class for Visp science calibration of polarized and non-polarized data.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    record_provenance = True

    def run(self):
        """
        Run Visp science calibration.

        - Collect all calibration objects
        - Process all frames
        - Record quality metrics


        Returns
        -------
        None

        """
        with self.apm_task_step("Loading calibration objects"):
            calibrations = self.collect_calibration_objects()

        with self.apm_task_step(
            f"Processing Science Frames for "
            f"{self.constants.num_map_scans} map scans and "
            f"{self.constants.num_raster_steps} raster steps"
        ):
            self.process_frames(calibrations=calibrations)

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_science_frames: int = self.scratch.count_all(
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("OBSERVE"),
                ],
            )

            self.quality_store_task_type_counts(
                task_type="OBSERVE", total_frames=no_of_raw_science_frames
            )

    def collect_calibration_objects(self) -> CalibrationCollection:
        """
        Collect *all* calibration for all beams, modstates, and exposure times.

        Doing this once here prevents lots of reads as we reduce the science data.
        """
        dark_dict = defaultdict(dict)
        solar_dict = defaultdict(dict)
        angle_dict = dict()
        state_offset_dict = defaultdict(dict)
        spec_shift_dict = dict()
        demod_dict = dict() if self.constants.correct_for_polarization else None

        for beam in range(1, self.constants.num_beams + 1):
            for exp_time in self.constants.observe_exposure_times:
                # Dark
                ######
                try:
                    dark_array = self.intermediate_frame_helpers_load_dark_array(
                        beam=beam, exposure_time=exp_time
                    )
                except StopIteration:
                    raise ValueError(f"No matching dark found for {exp_time = } s")

                dark_dict[VispTag.beam(beam)][VispTag.exposure_time(exp_time)] = dark_array

            # Angle
            #######
            angle_dict[VispTag.beam(beam)] = self.intermediate_frame_helpers_load_angle(beam=beam)

            # Spec shifts
            #############
            spec_shift_dict[VispTag.beam(beam)] = self.intermediate_frame_helpers_load_spec_shift(
                beam=beam
            )

            # Demod
            #######
            if self.constants.correct_for_polarization:
                demod_dict[
                    VispTag.beam(beam)
                ] = self.intermediate_frame_helpers_load_demod_matrices(beam_num=beam)

            for modstate in range(1, self.constants.num_modstates + 1):
                # Solar
                #######
                solar_dict[VispTag.beam(beam)][
                    VispTag.modstate(modstate)
                ] = self.intermediate_frame_helpers_load_solar_gain_array(
                    beam=beam, modstate=modstate
                )

                # State Offset
                ##############
                state_offset_dict[VispTag.beam(beam)][
                    VispTag.modstate(modstate)
                ] = self.intermediate_frame_helpers_load_state_offset(beam=beam, modstate=modstate)

        return CalibrationCollection(
            dark=dark_dict,
            solar_gain=solar_dict,
            angle=angle_dict,
            state_offset=state_offset_dict,
            spec_shift=spec_shift_dict,
            demod_matrices=demod_dict,
        )

    def process_frames(self, calibrations: CalibrationCollection):
        """
        Completely calibrate all science frames.

        - Apply all dark, gain, geometric corrections
        - Demodulate if needed
        - Combine beams
        - Apply telescope correction, if needed
        - Write calibrated arrays
        """
        for exp_time in self.constants.observe_exposure_times:
            for map_scan in range(1, self.constants.num_map_scans + 1):
                for raster_step in range(0, self.constants.num_raster_steps):
                    beam_storage = dict()
                    header_storage = dict()
                    for beam in range(1, self.constants.num_beams + 1):
                        apm_str = f"{map_scan = }, {raster_step = }, and {beam = }"
                        with self.apm_processing_step(f"Basic corrections for {apm_str}"):
                            # Initialize array_stack and headers
                            if self.constants.correct_for_polarization:
                                logging.info(
                                    f"Processing polarimetric observe frames from {apm_str}"
                                )
                                (
                                    intermediate_array,
                                    intermediate_header,
                                ) = self.process_polarimetric_modstates(
                                    beam=beam,
                                    raster_step=raster_step,
                                    map_scan=map_scan,
                                    exp_time=exp_time,
                                    calibrations=calibrations,
                                )
                            else:
                                logging.info(
                                    f"Processing spectrographic observe frames from {apm_str}"
                                )
                                intermediate_array, intermediate_header = self.correct_single_frame(
                                    beam=beam,
                                    modstate=1,
                                    raster_step=raster_step,
                                    map_scan=map_scan,
                                    exp_time=exp_time,
                                    calibrations=calibrations,
                                )
                                intermediate_header = self._compute_date_keys(intermediate_header)
                            beam_storage[VispTag.beam(beam)] = intermediate_array
                            header_storage[VispTag.beam(beam)] = intermediate_header

                    with self.apm_processing_step("Combining beams"):
                        logging.info("Combining beams")
                        calibrated = self.combine_beams(beam_storage, header_storage)

                    if self.constants.correct_for_polarization:
                        with self.apm_processing_step("Correcting telescope polarization"):
                            logging.info("Correcting telescope polarization")
                            calibrated = self.telescope_polarization_correction(calibrated)

                    # Save the final output files
                    with self.apm_writing_step("Writing calibrated arrays"):
                        logging.info("Writing calibrated arrays")
                        self.write_calibrated_array(calibrated, map_scan=map_scan)

    def process_polarimetric_modstates(
        self,
        beam: int,
        raster_step: int,
        map_scan: int,
        exp_time: float,
        calibrations: CalibrationCollection,
    ) -> Tuple[np.ndarray, fits.Header]:
        """
        Process a single polarimetric beam as much as is possible.

        This includes basic corrections and demodulation. Beam combination happens elsewhere.
        """
        # Create the 3D stack of corrected modulated arrays
        array_shape = calibrations.dark[VispTag.beam(1)][VispTag.exposure_time(exp_time)].shape
        array_stack = np.zeros(array_shape + (self.constants.num_modstates,))
        header_stack = []

        with self.apm_processing_step(f"Correcting {self.constants.num_modstates} modstates"):
            for modstate in range(1, self.constants.num_modstates + 1):
                # Correct the arrays
                corrected_array, corrected_header = self.correct_single_frame(
                    beam=beam,
                    modstate=modstate,
                    raster_step=raster_step,
                    map_scan=map_scan,
                    exp_time=exp_time,
                    calibrations=calibrations,
                )
                # Add this result to the 3D stack
                array_stack[:, :, modstate - 1] = corrected_array
                header_stack.append(corrected_header)

        with self.apm_processing_step("Applying instrument polarization correction"):
            logging.info("Applying instrument polarization correction")
            intermediate_array = self.polarization_correction(
                array_stack, calibrations.demod_matrices[VispTag.beam(beam)]
            )
            intermediate_header = self._compute_date_keys(header_stack)

        return intermediate_array, intermediate_header

    def combine_beams(self, array_dict: dict, header_dict: dict) -> VispL0FitsAccess:
        """
        Average all beams together.

        Also complain if the inputs are strange.
        """
        headers = list(header_dict.values())
        if len(headers) == 0:
            raise ValueError("No headers provided")
        for h in headers[1:]:
            if fits.HeaderDiff(headers[0], h):
                raise ValueError("Headers are different! This should NEVER happen!")

        array_list = []
        for beam in range(1, self.constants.num_beams + 1):
            array_list.append(array_dict[VispTag.beam(beam)])

        avg_array = average_numpy_arrays(array_list)

        hdu = fits.ImageHDU(data=avg_array, header=headers[0])
        obj = VispL0FitsAccess(hdu=hdu, auto_squeeze=False)

        return obj

    def write_calibrated_array(self, calibrated_object: VispL0FitsAccess, map_scan: int) -> None:
        """
        Write out calibrated science frames.

        For polarized data, write out calibrated science frames for all 4 Stokes parameters.
        For non-polarized data, write out calibrated science frames for Stokes I only.

        Parameters
        ----------
        calibrated_object
            Corrected frames object

        map_scan
            The current map scan. Needed because it's not a header key
        """
        if self.constants.correct_for_polarization:  # Write all 4 stokes params
            for i, stokes_param in enumerate(self.constants.stokes_params):
                final_data = self._re_dummy_data(calibrated_object.data[:, :, i])
                final_header = self._update_calibrated_header(
                    calibrated_object.header, map_scan=map_scan
                )
                self.write_cal_array(
                    data=final_data,
                    header=final_header,
                    stokes=stokes_param,
                    raster_step=calibrated_object.raster_scan_step,
                    map_scan=map_scan,
                )
        else:  # Only write stokes I
            final_data = self._re_dummy_data(calibrated_object.data)
            final_header = self._update_calibrated_header(
                calibrated_object.header, map_scan=map_scan
            )
            self.write_cal_array(
                data=final_data,
                header=final_header,
                stokes="I",
                raster_step=calibrated_object.raster_scan_step,
                map_scan=map_scan,
            )

    def correct_single_frame(
        self,
        beam: int,
        modstate: int,
        raster_step: int,
        map_scan: int,
        exp_time: float,
        calibrations: CalibrationCollection,
    ) -> Tuple[np.ndarray, fits.Header]:
        """
        Apply basic corrections to a single frame.

        Generally the algorithm is:
            1. Dark correct the array
            2. Solar Gain correct the array
            3. Geo correct the array
            4. Spectral correct array

        Parameters
        ----------
        beam
            The beam number for this single step
        modstate
            The modulator state for this single step
        raster_step
            The slit step for this single step
        map_scan
            The current map scan
        exp_time
            The exposure time for this single step
        calibrations
            Collection of all calibration objects

        Returns
        -------
            Corrected array, header
        """
        # Extract calibrations
        dark_array = calibrations.dark[VispTag.beam(beam)][VispTag.exposure_time(exp_time)]
        solar_gain_array = calibrations.solar_gain[VispTag.beam(beam)][VispTag.modstate(modstate)]
        angle = calibrations.angle[VispTag.beam(beam)]
        spec_shift = calibrations.spec_shift[VispTag.beam(beam)]
        state_offset = calibrations.state_offset[VispTag.beam(beam)][VispTag.modstate(modstate)]

        # Grab the input observe frame
        observe_object_list = list(
            self.input_frame_loaders_observe_fits_access_generator(
                map_scan=map_scan,
                raster_step=raster_step,
                modstate=modstate,
                exposure_time=exp_time,
            )
        )
        if len(observe_object_list) > 1:
            raise ValueError(
                f"Found more than one observe frame for {map_scan = }, {raster_step = }, {modstate = }, "
                f"and {exp_time = }. This should NEVER have happened!"
            )
        observe_object = observe_object_list[0]

        # Split the beam we want
        observe_data = self.input_frame_loaders_get_beam(observe_object.data, beam=beam)

        # Dark correction
        dark_corrected_array = next(subtract_array_from_arrays(observe_data, dark_array))

        # Gain correction
        gain_corrected_array = next(divide_arrays_by_array(dark_corrected_array, solar_gain_array))

        # Geo correction
        geo_corrected_array = next(
            self.corrections_correct_geometry(gain_corrected_array, state_offset, angle)
        )

        # Geo correction pt 2: spectral curvature
        spectral_corrected_array = next(
            self.corrections_remove_spec_geometry(geo_corrected_array, spec_shift)
        )

        return spectral_corrected_array, observe_object.header

    @staticmethod
    def polarization_correction(array_stack: np.ndarray, demod_matrices: np.ndarray) -> np.ndarray:
        """
        Apply a polarization correction to an array by multiplying the array stack by the demod matrices.

        Parameters
        ----------
        array_stack : np.ndarray
            (x, y, M) stack of corrected arrays with M modulation states

        demod_matrices : np.ndarray
            (x, y, 4, M) stack of demodulation matrices with 4 stokes planes and M modulation states


        Returns
        -------
        np.ndarray
            (x, y, 4) ndarray with the planes being IQUV
        """
        demodulated_array = np.sum(demod_matrices * array_stack[:, :, None, :], axis=3)
        return demodulated_array

    def telescope_polarization_correction(
        self,
        inst_demod_obj: VispL0FitsAccess,
    ) -> VispL0FitsAccess:
        """
        Apply a telescope polarization correction.

        Parameters
        ----------
        inst_demod_obj
            A demodulated, beam averaged frame
        telescope_db : str
            Telescope polarization correction loaded from telescope database

        Returns
        -------
        FitsAccess object with telescope corrections applied
        """
        tm = Telescope.from_fits_access(inst_demod_obj)
        mueller_matrix = tm.generate_inverse_telescope_model(M12=True, include_parallactic=True)
        inst_demod_obj.data = self.polarization_correction(inst_demod_obj.data, mueller_matrix)
        return inst_demod_obj

    @staticmethod
    def _compute_date_keys(headers: Union[Iterable[fits.Header], fits.Header]) -> fits.Header:
        """
        Generate correct DATE-??? header keys from a set of input headers.

        Keys are computed thusly:
        * DATE-BEG - The (Spec-0122) DATE-OBS of the earliest input header
        * DATE-END - The (Spec-0122) DATE-OBS of the latest input header, plus the FPA exposure time

        Returns
        -------
        fits.Header
            A copy of the earliest header, but with correct DATE-??? keys
        """
        if isinstance(headers, fits.Header) or isinstance(
            headers, fits.hdu.compressed.CompImageHeader
        ):
            headers = [headers]

        sorted_obj_list = sorted(
            [VispL0FitsAccess.from_header(h) for h in headers], key=lambda x: Time(x.time_obs)
        )
        date_beg = sorted_obj_list[0].time_obs
        exp_time = TimeDelta(sorted_obj_list[-1].fpa_exposure_time_ms / 1000.0, format="sec")
        date_end = (Time(sorted_obj_list[-1].time_obs) + exp_time).isot

        header = sorted_obj_list[0].header
        header["DATE-BEG"] = date_beg
        header["DATE-END"] = date_end

        return header

    def _re_dummy_data(self, data: np.ndarray):
        """
        Add the dummy dimension that we have been secretly squeezing out during processing.

        The dummy dimension is required because its corresponding WCS axis contains important information.

        Parameters
        ----------
        data : np.ndarray
            Corrected data
        """
        logging.debug(f"Adding dummy WCS dimension to array with shape {data.shape}")
        return data[None, :, :]

    def _update_calibrated_header(self, header: fits.Header, map_scan: int) -> fits.Header:
        """
        Update calibrated headers with any information gleaned during science calibration.

        Right now all this does is put map scan values in the header.

        Parameters
        ----------
        header
            The header to update

        map_scan
            Current map scan

        Returns
        -------
        fits.Header
        """
        header["VSPNMAPS"] = self.constants.num_map_scans
        header["VSPMAP"] = map_scan

        return header

    def write_cal_array(
        self,
        data: np.ndarray,
        header: fits.Header,
        stokes: str,
        raster_step: int,
        map_scan: int,
    ) -> None:
        """
        Write out calibrated array.

        Parameters
        ----------
        data : np.ndarray
            calibrated data to write out

        header : fits.Header
            calibrated header to write out

        stokes : str
            Stokes parameter of this step. 'I', 'Q', 'U', or 'V'

        raster_step : int
            The slit step for this step

        map_scan : int
            The current map scan


        Returns
        -------
        None
        """
        tags = [
            VispTag.calibrated(),
            VispTag.frame(),
            VispTag.stokes(stokes),
            VispTag.raster_step(raster_step),
            VispTag.map_scan(map_scan),
        ]
        hdul = fits.HDUList([fits.PrimaryHDU(header=header, data=data)])
        self.fits_data_write(hdu_list=hdul, tags=tags)

        filename = next(self.read(tags=tags))
        logging.info(f"Wrote intermediate file for {tags = } to {filename}")
