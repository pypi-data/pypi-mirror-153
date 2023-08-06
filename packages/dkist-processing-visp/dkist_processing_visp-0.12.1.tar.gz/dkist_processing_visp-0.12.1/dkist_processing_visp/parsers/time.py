"""Bud to find the exposure time."""
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.parsers.time import TaskExposureTimesBud

from dkist_processing_visp.parsers.task import parse_header_ip_task
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


class VispTaskExposureTimesBud(TaskExposureTimesBud):
    """
    Overload of common TaskExposureTimesBud to allow for custom ViSP parsing of ip_task_type.

    Parameters
    ----------
    stem_name : str
        The name of the stem of the tag
    ip_task_type : str
        Instrument program task type
    """

    def setter(self, fits_obj: VispL0FitsAccess):
        """
        Set the value of the bud.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        ip_task_type = parse_header_ip_task(fits_obj)  # This is where it's different
        if ip_task_type.lower() == self.ip_task_type.lower():
            raw_exp_time = getattr(fits_obj, self.metadata_key)
            return round(raw_exp_time, 6)
        return SpilledDirt
