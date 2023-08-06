"""ViSP raw data processing workflow."""
from dkist_processing_common.tasks import AddDatasetReceiptAccount
from dkist_processing_common.tasks import PublishCatalogAndQualityMessages
from dkist_processing_common.tasks import QualityL1Metrics
from dkist_processing_common.tasks import SubmitQuality
from dkist_processing_common.tasks import Teardown
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TransferL1Data
from dkist_processing_core import Workflow

from dkist_processing_visp.tasks.assemble_movie import AssembleVispMovie
from dkist_processing_visp.tasks.dark import DarkCalibration
from dkist_processing_visp.tasks.geometric import GeometricCalibration
from dkist_processing_visp.tasks.instrument_polarization import InstrumentPolarizationCalibration
from dkist_processing_visp.tasks.lamp import LampCalibration
from dkist_processing_visp.tasks.make_movie_frames import MakeVispMovieFrames
from dkist_processing_visp.tasks.parse import ParseL0VispInputData
from dkist_processing_visp.tasks.quality_metrics import VispL0QualityMetrics
from dkist_processing_visp.tasks.quality_metrics import VispL1QualityMetrics
from dkist_processing_visp.tasks.science import ScienceCalibration
from dkist_processing_visp.tasks.solar import SolarCalibration
from dkist_processing_visp.tasks.write_l1 import VispWriteL1Frame

l0_pipeline = Workflow(
    process_category="visp",
    process_name="l0_pipeline",
    workflow_package=__package__,
)
l0_pipeline.add_node(task=TransferL0Data, upstreams=None)
l0_pipeline.add_node(task=ParseL0VispInputData, upstreams=TransferL0Data)
l0_pipeline.add_node(task=VispL0QualityMetrics, upstreams=ParseL0VispInputData)
l0_pipeline.add_node(task=DarkCalibration, upstreams=ParseL0VispInputData)
l0_pipeline.add_node(task=LampCalibration, upstreams=DarkCalibration)
l0_pipeline.add_node(task=GeometricCalibration, upstreams=DarkCalibration)
l0_pipeline.add_node(task=SolarCalibration, upstreams=[LampCalibration, GeometricCalibration])
l0_pipeline.add_node(task=InstrumentPolarizationCalibration, upstreams=SolarCalibration)
l0_pipeline.add_node(task=ScienceCalibration, upstreams=InstrumentPolarizationCalibration)
l0_pipeline.add_node(task=VispWriteL1Frame, upstreams=ScienceCalibration)
l0_pipeline.add_node(task=QualityL1Metrics, upstreams=VispWriteL1Frame)
l0_pipeline.add_node(task=VispL1QualityMetrics, upstreams=VispWriteL1Frame)
l0_pipeline.add_node(
    task=SubmitQuality, upstreams=[VispL0QualityMetrics, QualityL1Metrics, VispL1QualityMetrics]
)
l0_pipeline.add_node(task=MakeVispMovieFrames, upstreams=VispWriteL1Frame)
l0_pipeline.add_node(task=AssembleVispMovie, upstreams=MakeVispMovieFrames)
l0_pipeline.add_node(task=AddDatasetReceiptAccount, upstreams=[AssembleVispMovie, SubmitQuality])
l0_pipeline.add_node(task=TransferL1Data, upstreams=AddDatasetReceiptAccount)
l0_pipeline.add_node(
    task=PublishCatalogAndQualityMessages,
    upstreams=TransferL1Data,
)
l0_pipeline.add_node(task=Teardown, upstreams=PublishCatalogAndQualityMessages)
