"""ViSP parse task."""
from typing import List
from typing import TypeVar

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.parsers.cs_step import CSStepFlower
from dkist_processing_common.parsers.cs_step import NumCSStepBud
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)
from dkist_processing_common.parsers.time import ExposureTimeFlower
from dkist_processing_common.parsers.unique_bud import UniqueBud
from dkist_processing_common.tasks import ParseL0InputData

from dkist_processing_visp.models.constants import VispBudName
from dkist_processing_visp.models.parameters import VispParameters
from dkist_processing_visp.models.tags import VispStemName
from dkist_processing_visp.parsers.map_repeats import MapScanFlower
from dkist_processing_visp.parsers.map_repeats import NumMapScansBud
from dkist_processing_visp.parsers.map_repeats import PickyMapBud
from dkist_processing_visp.parsers.polarimeter_mode import PolarimeterModeBud
from dkist_processing_visp.parsers.raster_step import RasterScanStepFlower
from dkist_processing_visp.parsers.raster_step import TotalRasterStepsBud
from dkist_processing_visp.parsers.spectral_line import SpectralLineBud
from dkist_processing_visp.parsers.task import VispTaskTypeFlower
from dkist_processing_visp.parsers.time import VispTaskExposureTimesBud
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess
from dkist_processing_visp.parsers.wavelength import ObserveWavelengthBud

S = TypeVar("S", bound=Stem)


class ParseL0VispInputData(ParseL0InputData):
    """
    Parse input ViSP data. Subclassed from the ParseL0InputData task in dkist_processing_common to add ViSP specific parameters.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        self.parameters = VispParameters(self.input_dataset_parameters)

    @property
    def fits_parsing_class(self):
        """FITS access class to use in this task."""
        return VispL0FitsAccess

    @property
    def constant_flowers(self) -> List[S]:
        """Add ViSP specific constants to common constants."""
        return super().constant_flowers + [
            PickyMapBud(),
            NumMapScansBud(),
            TotalRasterStepsBud(),
            NumCSStepBud(self.parameters.max_cs_step_time_sec),
            SpectralLineBud(),
            UniqueBud(
                constant_name=BudName.num_modstates.value, metadata_key="number_of_modulator_states"
            ),
            ObserveWavelengthBud(),
            PolarimeterModeBud(),
            VispTaskExposureTimesBud(
                stem_name=VispBudName.lamp_exposure_times.value, ip_task_type="LAMP_GAIN"
            ),
            VispTaskExposureTimesBud(
                stem_name=VispBudName.solar_exposure_times.value, ip_task_type="SOLAR_GAIN"
            ),
            VispTaskExposureTimesBud(
                stem_name=VispBudName.observe_exposure_times.value, ip_task_type="OBSERVE"
            ),
            VispTaskExposureTimesBud(
                stem_name=VispBudName.polcal_exposure_times.value, ip_task_type="POLCAL"
            ),
        ]

    @property
    def tag_flowers(self) -> List[S]:
        """Add ViSP specific tags to common tags."""
        return super().tag_flowers + [
            CSStepFlower(max_cs_step_time_sec=self.parameters.max_cs_step_time_sec),
            MapScanFlower(),
            VispTaskTypeFlower(),
            RasterScanStepFlower(),
            SingleValueSingleKeyFlower(
                tag_stem_name=VispStemName.modstate.value, metadata_key="modulator_state"
            ),
            ExposureTimeFlower(),
        ]
