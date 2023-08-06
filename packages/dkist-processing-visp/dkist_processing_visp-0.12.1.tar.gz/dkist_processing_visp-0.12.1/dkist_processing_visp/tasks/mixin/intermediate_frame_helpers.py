"""Helper to manage intermediate data."""
import logging
from typing import Generator
from typing import Iterable
from typing import Optional
from typing import TypeVar
from typing import Union

import numpy as np
from astropy.io import fits
from dkist_processing_common.models.fits_access import FitsAccessBase

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


class IntermediateFrameHelpersMixin:
    """Mixin for methods that support easy loading and writing of intermediate frames."""

    F = TypeVar("F", bound=FitsAccessBase)

    def intermediate_frame_helpers_load_intermediate_arrays(
        self,
        beam: Optional[int] = None,
        task: Optional[str] = None,
        modstate: Optional[int] = None,
        exposure_time: Optional[float] = None,
    ) -> Generator[np.ndarray, None, None]:
        """
        Yield a generator that produces ndarrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed
        task : str
            The task type of the data currently being processed
        modstate : int
            The current modulator state
        exposure_time : float
            The exposure time


        Returns
        -------
        Generator
            Array(s) of loaded intermediate data with requested tags
        """
        # See intermediate_frame_helpers_write_arrays for an explanation of how this works, to add new tags *all* that's needed
        # is to add a kwarg that has the same name as a tag
        passed_args = locals()
        tags = [VispTag.intermediate(), VispTag.frame()]
        for t, v in passed_args.items():
            if t not in ["self"] and v is not None:
                tags.append(getattr(VispTag, t)(v))

        for path, hdu in self.fits_data_read_hdu(tags=tags):
            yield hdu.data

    def intermediate_frame_helpers_load_dark_array(
        self, beam: Optional[int] = None, exposure_time: Optional[float] = None
    ) -> np.ndarray:
        """
        Produce dark ndarrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed
        exposure_time : float
            The exposure time


        Returns
        -------
        ndarray
            Array of loaded intermediate dark data with requested tags
        """
        return next(
            self.intermediate_frame_helpers_load_intermediate_arrays(
                beam=beam, task="DARK", exposure_time=exposure_time
            )
        )

    def intermediate_frame_helpers_load_lamp_gain_array(
        self, beam: Optional[int] = None, modstate: Optional[int] = None
    ) -> np.ndarray:
        """
        Produce lamp gain ndarrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state


        Returns
        -------
        ndarray
            Array of loaded intermediate lamp gain data with requested tags
        """
        return next(
            self.intermediate_frame_helpers_load_intermediate_arrays(
                beam=beam, task="LAMP_GAIN", modstate=modstate
            )
        )

    def intermediate_frame_helpers_load_solar_gain_array(
        self, beam: Optional[int] = None, modstate: Optional[int] = None
    ) -> np.ndarray:
        """
        Produce solar gain ndarrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state


        Returns
        -------
        ndarray
            Array of loaded intermediate solar gain data with requested tags
        """
        return next(
            self.intermediate_frame_helpers_load_intermediate_arrays(
                beam=beam, task="SOLAR_GAIN", modstate=modstate
            )
        )

    def intermediate_frame_helpers_load_demodulated_arrays(
        self, beam: Optional[int] = None, modstate: Optional[int] = None
    ) -> Generator[np.ndarray, None, None]:
        """
        Produce demodulated arrays for the requested tags.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state


        Returns
        -------
        Generator
            Array of loaded intermediate demodulated data with requested tags
        """
        return self.intermediate_frame_helpers_load_intermediate_arrays(
            beam=beam, task="DEMODULATED_ARRAYS", modstate=modstate
        )

    def intermediate_frame_helpers_write_arrays(
        self,
        arrays: Union[Iterable[np.ndarray], np.ndarray],
        headers: Optional[Union[Iterable[fits.Header], fits.Header]] = None,
        beam: Optional[int] = None,
        modstate: Optional[int] = None,
        map_scan: Optional[int] = None,
        raster_step: Optional[int] = None,
        task: Optional[str] = None,
        exposure_time: Optional[float] = None,
        file_id: Optional[str] = None,
    ) -> None:
        """
        Write out intermediate files with requested tags.

        Parameters
        ----------
        arrays
            pass
        headers
            pass
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state
        map_scan : int
             The current map scan
        raster_step : int
            The slit step for this step
        task : str
            The task type of the data currently being processed
        exposure_time : float
            The exposure time
        file_id:
            The unique file_id

        Returns
        -------
        None
        """
        # To add a new tag all you need to do is add a kwarg that has the same name as a tag. That's it!
        ## Construct the tags based on which optional parameters were passed
        passed_args = locals()
        tags = [VispTag.intermediate(), VispTag.frame()]
        for t, v in passed_args.items():
            # Look at all the arguments passed to this function, ignore those that aren't tags
            # and update tags with those that aren't None
            if t not in ["self", "arrays", "headers"] and v is not None:
                tags.append(getattr(VispTag, t)(v))

        arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
        if headers is not None:
            headers = [headers] if isinstance(headers, fits.Header) else headers
        else:
            # TODO: This len() stops us from passing arrays as a generator. Fix this.
            headers = [None] * len(arrays)

        for array, header in zip(arrays, headers):
            hdul = fits.HDUList([fits.PrimaryHDU(data=array, header=header)])
            self.fits_data_write(hdu_list=hdul, tags=tags)

        filenames = [str(p) for p in self.read(tags=tags)]
        logging.info(f"Wrote intermediate file for {tags = } to {filenames}")

    def intermediate_frame_helpers_load_demod_matrices(self, beam_num: int) -> np.ndarray:
        """
        Load demodulated matrices.

        Parameters
        ----------
        beam_num : int
            The current beam being processed


        Returns
        -------
        ndarray
            Demodulated matrix data
        """
        tags = [
            VispTag.intermediate(),
            VispTag.task("DEMOD_MATRICES"),
            VispTag.beam(beam_num),
        ]
        path, hdu = next(self.fits_data_read_hdu(tags=tags))
        return hdu.data

    def intermediate_frame_helpers_fits_access_generator(
        self,
        tags: Iterable[str],
    ) -> Generator[F, None, None]:
        """
        Load a generator of intermediate frames.

        Parameters
        ----------
        tags : str
            Requested tags for loading data

        Returns
        -------
        Generator
            generator of intermediate frames
        """
        tags += [VispTag.intermediate(), VispTag.frame()]
        frame_generator = self.fits_data_read_fits_access(tags, cls=VispL0FitsAccess)
        return frame_generator

    def intermediate_frame_helpers_load_angle(self, beam: int) -> float:
        """
        Load geometric angle for a given frame (beam).

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        float
            angle
        """
        angle_array = next(
            self.intermediate_frame_helpers_load_intermediate_arrays(
                beam=beam, task="GEOMETRIC_ANGLE"
            )
        )
        return angle_array[0]

    def intermediate_frame_helpers_load_state_offset(self, beam: int, modstate: int) -> np.ndarray:
        """
        Load state offset for a given beam and modstate.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state


        Returns
        -------
        ndarray
            state offset array
        """
        offset = next(
            self.intermediate_frame_helpers_load_intermediate_arrays(
                beam=beam, task="GEOMETRIC_OFFSET", modstate=modstate
            )
        )
        return offset

    def intermediate_frame_helpers_load_spec_shift(self, beam: int) -> np.ndarray:
        """
        Load spectral shift for a given beam.

        Parameters
        ----------
        beam : int
            The current beam being processed


        Returns
        -------
        ndarray
            spectral shift array
        """
        shifts = next(
            self.intermediate_frame_helpers_load_intermediate_arrays(
                beam=beam, task="GEOMETRIC_SPEC_SHIFTS"
            )
        )
        return shifts
