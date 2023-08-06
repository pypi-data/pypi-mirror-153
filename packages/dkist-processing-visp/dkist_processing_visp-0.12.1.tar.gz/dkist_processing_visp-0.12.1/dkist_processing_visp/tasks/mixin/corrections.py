"""Helper for ViSP array corrections."""
from typing import Generator
from typing import Iterable
from typing import Union

import numpy as np
import scipy.ndimage as spnd
from dkist_processing_math.transform import affine_transform_arrays
from dkist_processing_math.transform import rotate_arrays_about_point


class CorrectionsMixin:
    """Mixin to provide support for various array corrections used by the workflow tasks."""

    @staticmethod
    def corrections_correct_geometry(
        arrays: Union[Iterable[np.ndarray], np.ndarray],
        shift: np.ndarray = np.zeros(2),
        angle: float = 0.0,
    ) -> Generator[np.ndarray, None, None]:
        """
        Shift and then rotate data.

        It applies the inverse of the given shift and angle.

        Parameters
        ----------
        arrays
            2D array(s) containing the data for the un-shifted beam

        shift : np.ndarray
            The shift in the spectral dimension needed to "straighten" the spectra
            so a single wavelength is at the same pixel for all slit positions.

        angle : float
            The angle between slit hairlines and pixel axes.

        Returns
        -------
        Generator
            2D array(s) containing the data of the rotated and shifted beam
        """
        arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
        for array in arrays:
            array[np.where(array == np.inf)] = np.max(array[np.isfinite(array)])
            array[np.where(array == -np.inf)] = np.min(array[np.isfinite(array)])
            array[np.isnan(array)] = np.nanmedian(array)
            translated = affine_transform_arrays(
                array, translation=-shift, mode="constant", cval=np.nanmedian(array)
            )
            yield next(
                rotate_arrays_about_point(
                    translated, angle=-angle, mode="constant", cval=np.nanmedian(array)
                )
            )

    @staticmethod
    def corrections_remove_spec_geometry(
        arrays: Union[Iterable[np.ndarray], np.ndarray], spec_shift: np.ndarray
    ) -> Generator[np.ndarray, None, None]:
        """
        Remove spectral curvature.

        This is a pretty simple function that simply undoes the computed spectral shifts.

        Parameters
        ----------
        arrays
            2D array(s) containing the data for the un-distorted beam

        spec_shift : np.ndarray
            Array with shape (X), where X is the number of pixels in the spatial dimension.
            This dimension gives the spectral shift.

        Returns
        -------
        Generator
            2D array(s) containing the data of the corrected beam

        """
        arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
        for array in arrays:
            numy = array.shape[1]
            array_output = np.zeros(array.shape)
            for j in range(numy):
                array_output[:, j] = spnd.interpolation.shift(
                    array[:, j], -spec_shift[j], mode="constant", cval=np.nanmedian(array[:, j])
                )
            yield array_output
