"""Helper to manage input data."""
from typing import Generator
from typing import Optional
from typing import TypeVar

import numpy as np
from dkist_processing_common.models.fits_access import FitsAccessBase

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


class InputFrameLoadersMixin:
    """Mixin for methods that support easy loading of input frames."""

    F = TypeVar("F", bound=FitsAccessBase)

    def input_frame_loaders_fits_access_generator(
        self,
        beam: Optional[int] = None,
        modstate: Optional[int] = None,
        map_scan: Optional[int] = None,
        raster_step: Optional[int] = None,
        task: Optional[str] = None,
        cs_step: Optional[int] = None,
        exposure_time: Optional[float] = None,
    ) -> Generator[F, None, None]:
        """
        Load in intermediate fits frames.

        Parameters
        ----------
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
        cs_step : int
            The current cal sequence step
        exposure_time : float
            The exposure time


        Returns
        -------
        Generator
            Intermediate frames with correct tags
        """
        passed_args = locals()
        tags = [VispTag.input(), VispTag.frame()]
        for t, v in passed_args.items():
            if t not in ["self"] and v is not None:
                tags.append(getattr(VispTag, t)(v))

        frame_generator = self.fits_data_read_fits_access(tags, cls=VispL0FitsAccess)
        return frame_generator

    def input_frame_loaders_dark_array_generator(
        self, beam: Optional[int] = None, exposure_time: Optional[float] = None
    ) -> Generator[np.ndarray, None, None]:
        """
        Load in intermediate dark frames.

        Parameters
        ----------
        beam : int
            The current beam being processed
        exposure_time : float
            The exposure time


        Returns
        -------
        Generator
            Intermediate dark frames with correct tags
        """
        dark_array_fits_access = self.input_frame_loaders_fits_access_generator(
            task="DARK", exposure_time=exposure_time
        )
        for array in dark_array_fits_access:
            yield self.input_frame_loaders_get_beam(array.data, beam)

    def input_frame_loaders_lamp_gain_array_generator(
        self,
        beam: Optional[int] = None,
        modstate: Optional[int] = None,
        exposure_time: Optional[float] = None,
    ) -> Generator[np.ndarray, None, None]:
        """
        Load in intermediate lamp gain frames.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state
        exposure_time : float
            The exposure time


        Returns
        -------
        Generator
            Intermediate lamp gain frames with correct tags
        """
        lamp_gain_array_fits_access = self.input_frame_loaders_fits_access_generator(
            task="LAMP_GAIN", modstate=modstate, exposure_time=exposure_time
        )
        for array in lamp_gain_array_fits_access:
            yield self.input_frame_loaders_get_beam(array.data, beam)

    def input_frame_loaders_solar_gain_array_generator(
        self,
        beam: Optional[int] = None,
        modstate: Optional[int] = None,
        exposure_time: Optional[float] = None,
    ) -> Generator[np.ndarray, None, None]:
        """
        Load in intermediate solar gain frames.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state
        exposure_time : float
            The exposure time


        Returns
        -------
        Generator
            Intermediate solar gain frames with correct tags
        """
        solar_gain_array_fits_access = self.input_frame_loaders_fits_access_generator(
            task="SOLAR_GAIN", modstate=modstate, exposure_time=exposure_time
        )
        for array in solar_gain_array_fits_access:
            yield self.input_frame_loaders_get_beam(array.data, beam)

    def input_frame_loaders_observe_fits_access_generator(
        self,
        beam: Optional[int] = None,
        modstate: Optional[int] = None,
        raster_step: Optional[int] = None,
        map_scan: Optional[int] = None,
        exposure_time: Optional[float] = None,
    ) -> Generator[FitsAccessBase, None, None]:
        """
        Load in intermediate observe frames.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state
        raster_step : int
            The slit step for this step
        map_scan : int
             The current map scan
        exposure_time : float
            The exposure time


        Returns
        -------
        Generator
            Intermediate observe frames with correct tags
        """
        return self.input_frame_loaders_fits_access_generator(
            task="OBSERVE",
            beam=beam,
            modstate=modstate,
            raster_step=raster_step,
            map_scan=map_scan,
            exposure_time=exposure_time,
        )

    def input_frame_loaders_polcal_fits_access_generator(
        self,
        beam: Optional[int] = None,
        modstate: Optional[int] = None,
        cs_step: Optional[int] = None,
        exposure_time: Optional[float] = None,
    ) -> Generator[FitsAccessBase, None, None]:
        """
        Load in intermediate polcal frames.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state
        cs_step : int
            The current cal sequence step
        exposure_time : float
            The exposure time


        Returns
        -------
        Generator
            Intermediate polcal frames with correct tags
        """
        return self.input_frame_loaders_fits_access_generator(
            task="POLCAL",
            beam=beam,
            modstate=modstate,
            cs_step=cs_step,
            exposure_time=exposure_time,
        )

    def input_frame_loaders_get_beam(self, array: np.ndarray, beam: int) -> np.ndarray:
        """
        Extract a single beam array from a dual-beam array.

        Parameters
        ----------
        array
            The input dual-beam array
        beam
            The desired beam to extract

        Returns
        -------
        An ndarray containing the extracted beam
        """
        if beam == 1:
            return np.copy(array[: self.parameters.beam_border, ...])
        else:
            return np.copy(array[self.parameters.beam_border :, ...][::-1, :])
