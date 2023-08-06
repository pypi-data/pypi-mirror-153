"""ViSP task and subtask parser."""
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)

from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


def parse_header_ip_task(fits_obj: VispL0FitsAccess) -> str:
    """
    Parse ViSP tasks and subtasks.

    Parameters
    ----------
    fits_obj:
        A single FitsAccess object
    """
    if (
        fits_obj.ip_task_type == "gain"
        and fits_obj.gos_level3_status == "lamp"
        and fits_obj.gos_level3_lamp_status == "on"
    ):
        return "LAMP_GAIN"
    if fits_obj.ip_task_type == "gain" and fits_obj.gos_level3_status == "clear":
        return "SOLAR_GAIN"
    return fits_obj.ip_task_type


class VispTaskTypeFlower(SingleValueSingleKeyFlower):
    """Flower to find the ip task type."""

    def __init__(self):
        super().__init__(tag_stem_name=StemName.task.value, metadata_key="ip_task_type")

    def setter(self, fits_obj: VispL0FitsAccess):
        """
        Set value of the flower.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        return parse_header_ip_task(fits_obj)
