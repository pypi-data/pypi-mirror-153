from dataclasses import dataclass
from datetime import datetime
from typing import Tuple
from unittest.mock import patch
from unittest.mock import PropertyMock

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_pac.fitter.polcal_fitter import PolcalFitter
from dkist_processing_pac.input_data.dresser import Dresser

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.instrument_polarization import InstrumentPolarizationCalibration
from dkist_processing_visp.tests.conftest import FakeGQLClient
from dkist_processing_visp.tests.conftest import generate_fits_frame
from dkist_processing_visp.tests.conftest import VispConstantsDb
from dkist_processing_visp.tests.conftest import VispHeadersValidPolcalFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters


class DummyPolcalFitter(PolcalFitter):
    def __init__(self, num_modstates: int):
        with patch("dkist_processing_pac.fitter.polcal_fitter.PolcalDresserParameters"):
            super().__init__(
                dresser=Dresser(), fit_mode="use_M12", init_set="OCCal_VIS", _dont_fit=True
            )

        self.num_modstates = num_modstates

    @property
    def demodulation_matrices(self) -> np.ndarray:
        return np.ones((1, 1, 1, 4, self.num_modstates))


@dataclass
class VispInstPolCalTestingParameters(VispTestingParameters):
    visp_beam_border: int = 10


@pytest.fixture(scope="function")
def instrument_polarization_calibration_task(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db, mocker
):
    num_beams = 2
    num_modstates = 2
    num_cs_steps = 2
    exposure_time = 0.01  # From VispHeadersValidPolcalFrames fixture
    intermediate_shape = (10, 10)
    dataset_shape = (num_cs_steps, 20, 10)
    array_shape = (1, 20, 10)
    constants_db = VispConstantsDb(
        POLARIMETER_MODE="observe_polarimetric",
        NUM_MODSTATES=num_modstates,
        NUM_BEAMS=num_beams,
        NUM_CS_STEPS=num_cs_steps,
        POLCAL_EXPOSURE_TIMES=(exposure_time,),
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with InstrumentPolarizationCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="instrument_polarization_calibration",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            assign_input_dataset_doc_to_task(task, VispInstPolCalTestingParameters())
            all_zeros = np.zeros(intermediate_shape)
            all_ones = np.ones(intermediate_shape)
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )

            mocker.patch(
                "dkist_processing_visp.tasks.instrument_polarization.PolcalFitter",
                new_callable=PropertyMock,
                return_value=DummyPolcalFitter(num_modstates),
            )

            # Don't test place-holder QA stuff for now
            mocker.patch(
                "dkist_processing_visp.tasks.instrument_polarization.InstrumentPolarizationCalibration.record_polcal_quality_metrics"
            )
            # Create fake geometric objects
            angle = np.array([0.0])
            offset = np.array([0.0, 0.0])
            spec_shift = np.zeros(intermediate_shape[0])
            for beam in range(1, num_beams + 1):
                task.intermediate_frame_helpers_write_arrays(
                    arrays=angle, beam=beam, task="GEOMETRIC_ANGLE"
                )
                task.intermediate_frame_helpers_write_arrays(
                    arrays=spec_shift, beam=beam, task="GEOMETRIC_SPEC_SHIFTS"
                )
                for modstate in range(1, num_modstates + 1):
                    task.intermediate_frame_helpers_write_arrays(
                        arrays=offset, beam=beam, modstate=modstate, task="GEOMETRIC_OFFSET"
                    )

            # Create fake dark intermediate arrays
            for beam in range(1, num_beams + 1):
                task.intermediate_frame_helpers_write_arrays(
                    all_zeros, beam=beam, task="DARK", exposure_time=exposure_time
                )

            for beam in range(1, num_beams + 1):
                # Create a fake solar gain array for this beam and modstate
                for modstate in range(1, num_modstates + 1):
                    gain_hdul = fits.HDUList([fits.PrimaryHDU(data=all_ones)])
                    task.fits_data_write(
                        hdu_list=gain_hdul,
                        tags=[
                            VispTag.intermediate(),
                            VispTag.frame(),
                            VispTag.task("SOLAR_GAIN"),
                            VispTag.beam(beam),
                            VispTag.modstate(modstate),
                            VispTag.exposure_time(exposure_time),
                        ],
                    )

            start_time = datetime.now()
            for modstate in range(1, num_modstates + 1):
                # Create polcal input frames for this modstate
                ds = VispHeadersValidPolcalFrames(
                    dataset_shape=dataset_shape,
                    array_shape=array_shape,
                    time_delta=10,
                    num_modstates=num_modstates,
                    modstate=modstate,
                    start_time=start_time,
                )
                header_generator = (
                    spec122_validator.validate_and_translate_to_214_l0(
                        d.header(), return_type=fits.HDUList
                    )[0].header
                    for d in ds
                )
                # cs_step does not map to a single keyword, so not needed in the fake headers
                for cs_step in range(num_cs_steps):
                    hdul = generate_fits_frame(header_generator=header_generator, shape=array_shape)
                    task.fits_data_write(
                        hdu_list=hdul,
                        tags=[
                            VispTag.task("POLCAL"),
                            VispTag.modstate(modstate),
                            VispTag.cs_step(cs_step),
                            VispTag.input(),
                            VispTag.frame(),
                            VispTag.exposure_time(exposure_time),
                        ],
                    )

            yield task
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


@pytest.fixture(scope="function")
def instrument_polarization_calibration_task_with_no_data(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db
):
    init_visp_constants_db(recipe_run_id, VispConstantsDb())
    with InstrumentPolarizationCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="instrument_polarization_calibration",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            assign_input_dataset_doc_to_task(task, VispInstPolCalTestingParameters())
            yield task
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


@pytest.fixture()
def full_beam_shape() -> Tuple[int, int]:
    return (1000, 2560)


@pytest.fixture()
def single_demodulation_matrix() -> np.ndarray:
    return np.arange(40).reshape(1, 1, 1, 4, 10)


@pytest.fixture()
def multiple_demodulation_matrices() -> np.ndarray:
    return np.arange(2 * 3 * 4 * 10).reshape(1, 2, 3, 4, 10)


def test_instrument_polarization_calibration_task(instrument_polarization_calibration_task, mocker):
    """
    Given: An InstrumentPolarizationCalibration task
    When: Calling the task instance
    Then: A demodulation matrix for each beam is produced
    """

    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )

    # When
    task = instrument_polarization_calibration_task
    task()

    # Then
    for beam in range(1, 2 + 1):
        tags = [
            VispTag.intermediate(),
            VispTag.task("DEMOD_MATRICES"),
            VispTag.beam(beam),
        ]
        assert len(list(task.read(tags=tags))) == 1


def test_reshape_demod_matrices(
    instrument_polarization_calibration_task_with_no_data,
    multiple_demodulation_matrices,
    full_beam_shape,
):
    """
    Given: An InstrumentPolarizationCalibration task and a set of demodulation matrices sampled over the full FOV
    When: Up-sampling the demodulation matrices
    Then: The final set of demodulation matrices has the correct, full-FOV shape
    """
    instrument_polarization_calibration_task_with_no_data.single_beam_shape = full_beam_shape
    result = instrument_polarization_calibration_task_with_no_data.reshape_demod_matrices(
        multiple_demodulation_matrices
    )
    assert result.shape == full_beam_shape + (4, 10)


def test_reshape_single_demod_matrix(
    instrument_polarization_calibration_task_with_no_data,
    single_demodulation_matrix,
    full_beam_shape,
):
    """
    Given: An InstrumentPolarizationCalibration task and a single demodulation matrix for the whole FOV
    When: Up-sampling the demodulation matrices
    Then: The final set of demodulation matrices still only has a single matrix
    """
    instrument_polarization_calibration_task_with_no_data.single_beam_shape = full_beam_shape
    result = instrument_polarization_calibration_task_with_no_data.reshape_demod_matrices(
        single_demodulation_matrix
    )
    assert result.shape == (4, 10)
