"""Visp spectral line parser."""
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.spectral_line import find_associated_line
from dkist_processing_common.parsers.unique_bud import UniqueBud

from dkist_processing_visp.models.spectral_line import VISP_SPECTRAL_LINES
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


class SpectralLineBud(UniqueBud):
    """Get spectral line wavelengths from file metadata."""

    def __init__(self):
        super().__init__(constant_name=BudName.spectral_line.value, metadata_key="wavelength")

    def setter(self, fits_obj: VispL0FitsAccess):
        """
        Given a list of SpectralLine objects, find the one that contains the wavelength of the frame within its range, and return its name for observe frames only.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt
        return find_associated_line(wavelength=fits_obj.wavelength, lines=VISP_SPECTRAL_LINES)
