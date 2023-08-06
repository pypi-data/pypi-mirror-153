"""ViSP instrument polarization task."""
import logging
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Tuple

import numpy as np
from astropy.io import fits
from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_processing_math.arithmetic import divide_arrays_by_array
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from dkist_processing_math.transform.binning import resize_arrays
from dkist_processing_pac.fitter.fitting_core import fill_modulation_matrix
from dkist_processing_pac.fitter.fitting_core import generate_model_I
from dkist_processing_pac.fitter.fitting_core import generate_S
from dkist_processing_pac.fitter.polcal_fitter import PolcalFitter
from dkist_processing_pac.input_data.drawer import Drawer
from dkist_processing_pac.input_data.dresser import Dresser

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess
from dkist_processing_visp.tasks.mixin.corrections import CorrectionsMixin
from dkist_processing_visp.tasks.mixin.input_frame_loaders import InputFrameLoadersMixin
from dkist_processing_visp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_visp.tasks.visp_base import VispTaskBase


class InstrumentPolarizationCalibration(
    VispTaskBase,
    IntermediateFrameHelpersMixin,
    InputFrameLoadersMixin,
    CorrectionsMixin,
    QualityMixin,
):
    """
    Task class for instrument polarization for a VISP calibration run.

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

    def run(self) -> None:
        """
        For each beam.

            - Reduce calibration sequence steps
            - Fit reduced data to PAC parameters
            - Compute and save demodulation matrices

        Returns
        -------
        None

        """
        # TODO: There might be a better way to skip this task
        if not self.constants.correct_for_polarization:
            return

        # Process the pol cal frames
        logging.info(
            f"Demodulation matrices will span FOV with shape {(self.parameters.polcal_num_spectral_bins, self.parameters.polcal_num_spatial_bins)}"
        )
        for beam in range(1, self.constants.num_beams + 1):
            with self.apm_processing_step(f"Reducing CS steps for {beam = }"):
                reduced_arrays = self.reduce_cs_steps(beam)

            with self.apm_processing_step(f"Fit CU parameters for {beam = }"):
                logging.info(f"Fit CU parameters for {beam = }")
                dresser = Dresser()
                dresser.add_drawer(Drawer(reduced_arrays))
                pac_fitter = PolcalFitter(
                    dresser=dresser,
                    fit_mode=self.parameters.pac_fit_mode,
                    init_set=self.parameters.pac_init_set,
                    fit_TM=False,
                )

            with self.apm_processing_step(f"Resampling demodulation matrices for {beam = }"):
                demod_matrices = pac_fitter.demodulation_matrices
                # Reshaping the demodulation matrix to get rid of unit length dimensions
                logging.info(f"Resampling demodulation matrices for {beam = }")
                demod_matrices = self.reshape_demod_matrices(demod_matrices)
                logging.info(f"Shape of resampled demodulation matrices: {demod_matrices.shape}")

            with self.apm_writing_step(f"Writing demodulation matrices for {beam = }"):
                # Save the demod matrices as intermediate products
                self.intermediate_frame_helpers_write_arrays(
                    demod_matrices,
                    beam=beam,
                    task="DEMOD_MATRICES",
                )

            with self.apm_processing_step("Computing and recording polcal quality metrics"):
                self.record_polcal_quality_metrics(beam, polcal_fitter=pac_fitter)

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_polcal_frames: int = self.scratch.count_all(
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("POLCAL"),
                ],
            )

            self.quality_store_task_type_counts(
                task_type="polcal", total_frames=no_of_raw_polcal_frames
            )

    def reduce_cs_steps(self, beam: int) -> Dict[int, List[VispL0FitsAccess]]:
        """
        Reduce all of the data for the cal sequence steps for this beam.

        Parameters
        ----------
        beam
            The current beam being processed

        Returns
        -------
        Dict
            A Dict of calibrated and binned arrays for all the cs steps for this beam
        """
        # Create the dict to hold the results
        reduced_arrays = defaultdict(list)

        for modstate in range(1, self.constants.num_modstates + 1):
            angle = self.intermediate_frame_helpers_load_angle(beam=beam)
            state_offset = self.intermediate_frame_helpers_load_state_offset(
                beam=beam, modstate=modstate
            )
            spec_shift = self.intermediate_frame_helpers_load_spec_shift(beam=beam)

            for exp_time in self.constants.polcal_exposure_times:
                # Put this loop here because the geometric objects will be constant across exposure times
                logging.info(f"Loading dark for {exp_time = } and {beam = }")
                try:
                    dark_array = self.intermediate_frame_helpers_load_dark_array(
                        beam, exposure_time=exp_time
                    )
                except StopIteration:
                    raise ValueError(f"No matching dark found for {exp_time = } s")

                for cs_step in range(self.constants.num_cs_steps):
                    reduced_arrays[cs_step].append(
                        self.reduce_single_step(
                            beam,
                            dark_array,
                            modstate,
                            cs_step,
                            exp_time,
                            angle,
                            state_offset,
                            spec_shift,
                        )
                    )

        return reduced_arrays

    def reduce_single_step(
        self,
        beam: int,
        dark_array: np.ndarray,
        modstate: int,
        cs_step: int,
        exp_time: float,
        angle: float,
        state_offset: np.ndarray,
        spec_shift: np.ndarray,
    ) -> VispL0FitsAccess:
        """
        Reduce a single calibration step for this beam, cs step and modulator state.

        Parameters
        ----------
        beam : int
            The current beam being processed
        dark_array : np.ndarray
            The dark array for the current beam
        modstate : int
            The current modulator state
        cs_step : int
            The current cal sequence step
        exp_time : float
            The exposure time
        angle : float
            The beam angle for the current modstate
        state_offset : np.ndarray
            The state offset for the current modstate
        spec_shift : np.ndarray
            The spectral shift for the current modstate

        Returns
        -------
        The final reduced result for this single step
        """
        apm_str = f"{beam = }, {modstate = }, {cs_step = }, and {exp_time = }"
        logging.info(f"Reducing {apm_str}")
        # Get the iterable of objects for this beam, cal seq step and mod state

        # Get the headers and arrays as iterables
        pol_cal_headers = (
            obj.header
            for obj in self.input_frame_loaders_polcal_fits_access_generator(
                modstate=modstate, cs_step=cs_step, exposure_time=exp_time
            )
        )
        pol_cal_arrays = (
            self.input_frame_loaders_get_beam(obj.data, beam)
            for obj in self.input_frame_loaders_polcal_fits_access_generator(
                modstate=modstate, cs_step=cs_step, exposure_time=exp_time
            )
        )
        # Grab the 1st header
        avg_inst_pol_cal_header = next(pol_cal_headers)

        # Average the arrays (this works for a single array as well)
        avg_inst_pol_cal_array = average_numpy_arrays(pol_cal_arrays)

        with self.apm_processing_step(f"Apply basic corrections for {apm_str}"):
            dark_corrected_array = subtract_array_from_arrays(avg_inst_pol_cal_array, dark_array)

            solar_gain_array = self.intermediate_frame_helpers_load_solar_gain_array(
                beam=beam, modstate=modstate
            )
            gain_corrected_array = next(
                divide_arrays_by_array(dark_corrected_array, solar_gain_array)
            )

            geo_corrected_array = self.corrections_correct_geometry(
                gain_corrected_array, -state_offset, angle
            )

            spectral_corrected_array = self.corrections_remove_spec_geometry(
                geo_corrected_array, spec_shift
            )

        with self.apm_processing_step(f"Extract macro pixels from {apm_str}"):
            self._set_original_beam_size(gain_corrected_array)
            output_shape = (
                self.parameters.polcal_num_spectral_bins,
                self.parameters.polcal_num_spatial_bins,
            )
            binned_array = next(resize_arrays(spectral_corrected_array, output_shape))

        with self.apm_processing_step(f"Create reduced VispL0FitsAccess for {apm_str}"):
            result = VispL0FitsAccess(
                fits.ImageHDU(binned_array[None, :, :], avg_inst_pol_cal_header), auto_squeeze=False
            )

        return result

    def reshape_demod_matrices(self, demod_matrices: np.ndarray) -> np.ndarray:
        """Upsample demodulation matrices to match the full beam size.

        Given an input set of demodulation matrices with shape (1, X', Y', 4, M) resample the output to shape
        (X, Y, 4, M), where X' and Y' are the binned size of the beam FOV, X and Y are the full beam shape, M is the
        number of modulator states, and 1 is the PA&C dummy dimension,

        If only a single demodulation matrix was made then it is returned as a single array with shape (4, M).

        Parameters
        ----------
        demod_matrices
            A set of demodulation matrices with shape (1, X', Y', 4, M)

        Returns
        -------
        If X' and Y' > 1 then upsampled matrices that are the full beam size (X, Y, 4, M).
        If X' == Y' == 1 then a single matric for the whole FOV with shape (4, M)
        """
        if len(demod_matrices.shape) != 5:
            raise ValueError(
                f"Expected demodulation matrices to have 5 dimensions. Got shape {demod_matrices.shape}"
            )

        # For ViSP, the first dimension is always a dummy. See the last lines of reduce_single_step
        sliced_demod = demod_matrices[0, :, :, :, :]
        data_shape = sliced_demod.shape[:2]  # The non-demodulation matrix part of the larger array
        demod_shape = sliced_demod.shape[-2:]  # The shape of a single demodulation matrix
        logging.info(f"Demodulation FOV sampling shape: {data_shape}")
        logging.info(f"Demodulation matrix shape: {demod_shape}")
        if data_shape == (1, 1):
            # A single modulation matrix can be used directly, so just return it after removing extraneous dimensions
            logging.info(f"Single demodulation matrix detected")
            return sliced_demod[0, 0, :, :]

        target_shape = self.single_beam_shape + demod_shape
        logging.info(f"Target full-frame demodulation shape: {target_shape}")
        return self._resize_polcal_array(sliced_demod, target_shape)

    # TODO: Put more/real stuff here
    # TODO: Add test coverage?
    def record_polcal_quality_metrics(
        self,
        beam: int,
        polcal_fitter: PolcalFitter,
    ) -> None:
        """Record various quality metrics from PolCal fits.

        THIS FUNCTION IS INCOMPLETE. Right now it just saves some files for manual inspection.
        """
        dresser = polcal_fitter.dresser
        ## Input flux
        #############
        input_flux_tags = [
            VispTag.intermediate(),
            VispTag.beam(beam),
            VispTag.task("INPUT_FLUX"),
        ]

        # Put all flux into a single array
        fov_shape = dresser.shape
        socc_shape = (dresser.numdrawers, dresser.drawer_step_list[0], self.constants.num_modstates)
        flux_shape = fov_shape + socc_shape
        input_flux = np.zeros(flux_shape, dtype=np.float64)
        for i in range(np.prod(fov_shape)):
            idx = np.unravel_index(i, fov_shape)
            I_cal, _ = dresser[idx]
            input_flux[idx] = I_cal.T.reshape(socc_shape)

        flux_hdl = fits.HDUList([fits.PrimaryHDU(input_flux)])
        with self.apm_writing_step("Writing input flux"):
            self.fits_data_write(hdu_list=flux_hdl, tags=input_flux_tags)
            logging.info(
                f"Wrote input flux with tags {input_flux_tags = } to {next(self.read(tags=input_flux_tags))}"
            )

        ## Calibration Unit best fit parameters
        #######################################
        # cmp_tags = [
        #     VispTag.intermediate(),
        #     VispTag.beam(beam),
        #     VispTag.task("CU_FIT_PARS"),
        # ]
        # with self.apm_writing_step("Writing CU fit parameters"):
        #     self.fits_data_write(hdu_list=dc_cmp.hdu_list, tags=cmp_tags)
        #     logging.info(f"Wrote CU fits with {cmp_tags = } to {next(self.read(tags=cmp_tags))}")

        ## Best-fix flux
        ################
        fit_flux_tags = [VispTag.intermediate(), VispTag.beam(beam), VispTag.task("BEST_FIT_FLUX")]
        with self.apm_processing_step("Computing best-fit flux"):
            best_fit_flux = self.compute_best_fit_flux(polcal_fitter)
            best_fit_hdl = fits.HDUList([fits.PrimaryHDU(best_fit_flux)])

        with self.apm_writing_step("Writing best-fit flux"):
            self.fits_data_write(hdu_list=best_fit_hdl, tags=fit_flux_tags)
            logging.info(
                f"Wrote best-fit flux with {fit_flux_tags = } to {next(self.read(tags=fit_flux_tags))}"
            )

    # TODO: Test coverage? Hard to do.
    def compute_best_fit_flux(self, polcal_fitter: PolcalFitter) -> np.ndarray:
        """Calculate the best-fit SoCC flux from a set of fit parameters.

        The output array has shape (1, num_spectral_bins, num_spatial_bins, 1, 4, num_modstate)
        """
        dresser = polcal_fitter.dresser
        fov_shape = dresser.shape
        socc_shape = (dresser.numdrawers, dresser.drawer_step_list[0], self.constants.num_modstates)
        flux_shape = fov_shape + socc_shape
        best_fit_flux = np.zeros(flux_shape, dtype=np.float64)
        num_points = np.prod(fov_shape)
        for i in range(num_points):
            idx = np.unravel_index(i, fov_shape)
            I_cal, _ = dresser[idx]
            CM = polcal_fitter.CM
            TM = polcal_fitter.TM
            par_vals = polcal_fitter.fit_parameters[idx].valuesdict()
            CM.load_pars_from_dict(par_vals)
            TM.load_pars_from_dict(par_vals)
            S = generate_S(TM=TM, CM=CM, use_M12=True)
            O = fill_modulation_matrix(par_vals, np.zeros((dresser.nummod, 4)))
            I_mod = generate_model_I(O, S)

            # Save all data to associated arrays
            best_fit_flux[idx] = I_mod.T.reshape(socc_shape)

        return best_fit_flux

    def _set_original_beam_size(self, array: np.ndarray) -> None:
        """Record the shape of a single beam as a class property."""
        self.single_beam_shape = array.shape

    def _resize_polcal_array(self, array: np.ndarray, output_shape: Tuple[int, ...]) -> np.ndarray:
        return next(resize_arrays(array, output_shape))
