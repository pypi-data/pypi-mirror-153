import json
from dataclasses import dataclass

import numpy as np
import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.solar import SolarCalibration
from dkist_processing_visp.tests.conftest import FakeGQLClient
from dkist_processing_visp.tests.conftest import generate_214_l0_fits_frame
from dkist_processing_visp.tests.conftest import VispConstantsDb
from dkist_processing_visp.tests.conftest import VispHeadersValidSolarGainFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters


@dataclass
class VispSolarTestingParameters(VispTestingParameters):
    visp_beam_border: int = 10


@pytest.fixture(scope="function")
def solar_gain_calibration_task_that_completes(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db
):
    number_of_modstates = 3
    number_of_beams = 2
    exposure_time = 20.0  # From VispHeadersValidSolarGainFrames fixture
    intermediate_shape = (10, 10)
    dataset_shape = (1, 20, 10)
    array_shape = (1, 20, 10)
    constants_db = VispConstantsDb(
        NUM_MODSTATES=number_of_modstates, SOLAR_EXPOSURE_TIMES=(exposure_time,)
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with SolarCalibration(
        recipe_run_id=recipe_run_id, workflow_name="geometric_calibration", workflow_version="VX.Y"
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispSolarTestingParameters())
            for beam in range(1, number_of_beams + 1):

                # DarkCal object
                dark_cal = np.ones(intermediate_shape) * 3.0
                task.intermediate_frame_helpers_write_arrays(
                    arrays=dark_cal, beam=beam, task="DARK", exposure_time=exposure_time
                )

                # Geo angles and spec_shifts
                task.intermediate_frame_helpers_write_arrays(
                    arrays=np.zeros(1), beam=beam, task="GEOMETRIC_ANGLE"
                )
                task.intermediate_frame_helpers_write_arrays(
                    arrays=np.zeros(intermediate_shape[0]), beam=beam, task="GEOMETRIC_SPEC_SHIFTS"
                )

                for modstate in range(1, number_of_modstates + 1):
                    # LampCal object
                    lamp_cal = np.ones(intermediate_shape) * 10 * modstate * beam
                    task.intermediate_frame_helpers_write_arrays(
                        arrays=lamp_cal, beam=beam, modstate=modstate, task="LAMP_GAIN"
                    )

                    # Geo offsets
                    task.intermediate_frame_helpers_write_arrays(
                        arrays=np.zeros(2), beam=beam, modstate=modstate, task="GEOMETRIC_OFFSET"
                    )

                    ds = VispHeadersValidSolarGainFrames(
                        dataset_shape=dataset_shape,
                        array_shape=array_shape,
                        time_delta=10,
                        num_modstates=number_of_modstates,
                        modstate=modstate,
                    )
                    header = ds.header()
                    true_gain = np.ones(array_shape[1:]) + modstate + beam
                    true_solar_signal = np.arange(1, array_shape[1] + 1) / 5
                    true_solar_gain = true_gain * true_solar_signal[:, None]
                    raw_lamp = np.concatenate((lamp_cal, lamp_cal))
                    raw_dark = np.concatenate((dark_cal, dark_cal))
                    raw_solar = (true_solar_gain * raw_lamp) + raw_dark
                    solar_hdul = generate_214_l0_fits_frame(data=raw_solar, s122_header=header)
                    task.fits_data_write(
                        hdu_list=solar_hdul,
                        tags=[
                            VispTag.input(),
                            VispTag.task("SOLAR_GAIN"),
                            VispTag.modstate(modstate),
                            VispTag.frame(),
                            VispTag.beam(beam),
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
def solar_gain_calibration_task_with_no_data(tmp_path, recipe_run_id, init_visp_constants_db):
    number_of_modstates = 3
    constants_db = VispConstantsDb(NUM_MODSTATES=number_of_modstates)
    init_visp_constants_db(recipe_run_id, constants_db)
    with SolarCalibration(
        recipe_run_id=recipe_run_id, workflow_name="geometric_calibration", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)

        yield task
        task.scratch.purge()
        task.constants._purge()


def test_solar_gain_task(solar_gain_calibration_task_that_completes, mocker):
    """
    Given: A set of raw solar gain images and necessary intermediate calibrations
    When: Running the solargain task
    Then: The task completes and the outputs are correct
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )

    # It's way too hard to make data for a unit test that get through the line zones calculation.
    # Leave that for grogu.
    mocker.patch(
        "dkist_processing_visp.tasks.solar.SolarCalibration.compute_line_zones",
        return_value=[(4, 7)],
    )
    task = solar_gain_calibration_task_that_completes
    task()
    for beam in range(1, task.constants.num_beams + 1):
        for modstate in range(1, task.constants.num_modstates + 1):
            expected = np.ones((10, 10)) * 10 * modstate * beam
            solar_gain = task.intermediate_frame_helpers_load_solar_gain_array(
                beam=beam, modstate=modstate
            )
            np.testing.assert_allclose(expected, solar_gain)

    quality_files = task.read(tags=[Tag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[VispTag.input(), VispTag.frame(), VispTag.task("SOLAR_GAIN")]
            )


def test_line_zones(solar_gain_calibration_task_with_no_data):
    """
    Given: A spectrum with some absorption lines
    When: Computing zones around the lines
    Then: Correct results are returned
    """
    # This is here because we mocked it out in the solar gain task test above
    # NOTE that it does not test for removal of overlapping regions
    def gaussian(x, amp, mu, sig):
        return amp * np.exp(-np.power(x - mu, 2.0) / (2 * np.power(sig, 2.0)))

    spec = np.ones(1000) * 100
    x = np.arange(1000.0)
    expected = []
    for m, s in zip([100.0, 300.0, 700], [10.0, 20.0, 5.0]):
        spec -= gaussian(x, 40, m, s)
        hwhm = s * 2.355 / 2
        expected.append((np.floor(m - hwhm).astype(int), np.ceil(m + hwhm).astype(int)))

    zones = solar_gain_calibration_task_with_no_data.compute_line_zones(
        spec[:, None], bg_order=0, rel_height=0.5
    )
    assert zones == expected


def test_identify_overlapping_zones(solar_gain_calibration_task_with_no_data):
    """
    Given: A list of zone borders that contain overlapping zones
    When: Identifying zones that overlap
    Then: The smaller of the overlapping zones are identified for removal
    """
    rips = np.array([100, 110, 220, 200])
    lips = np.array([150, 120, 230, 250])

    idx_to_remove = solar_gain_calibration_task_with_no_data.identify_overlapping_zones(rips, lips)
    assert idx_to_remove == [1, 2]
