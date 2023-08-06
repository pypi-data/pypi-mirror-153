import re
from datetime import datetime
from datetime import timedelta
from itertools import chain

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator.translator import translate_spec122_to_spec214_l0
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag

from dkist_processing_visp.tasks.parse import ParseL0VispInputData
from dkist_processing_visp.tests.conftest import FakeGQLClient
from dkist_processing_visp.tests.conftest import VispHeadersValidDarkFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidLampGainFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidObserveFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidPolcalFrames
from dkist_processing_visp.tests.conftest import VispHeadersValidSolarGainFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters


@pytest.fixture(scope="function")
def parse_inputs_valid_task(tmp_path, recipe_run_id, assign_input_dataset_doc_to_task):
    num_maps = 1
    num_modstates = 2
    num_steps = 3
    with ParseL0VispInputData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            ds1 = VispHeadersValidDarkFrames(
                dataset_shape=(2, 2, 2), array_shape=(1, 2, 2), time_delta=10
            )
            ds2 = VispHeadersValidLampGainFrames(
                dataset_shape=(2, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=10,
                num_modstates=2,
                modstate=1,
            )
            ds3 = VispHeadersValidSolarGainFrames(
                dataset_shape=(2, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=10,
                num_modstates=2,
                modstate=1,
            )
            ds4 = VispHeadersValidPolcalFrames(
                dataset_shape=(2, 2, 2),
                array_shape=(2, 2, 1),
                time_delta=30,
                num_modstates=2,
                modstate=1,
            )
            ds = chain(ds1, ds2, ds3, ds4)
            for d in ds:
                header = d.header()
                translated_header = translate_spec122_to_spec214_l0(header)
                hdu = fits.PrimaryHDU(
                    data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                )
                hdul = fits.HDUList([hdu])
                task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])

            start_time = datetime.now()
            time_delta = timedelta(seconds=10)
            i = 0
            for map_scan in range(1, num_maps + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(num_steps):
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_raster_steps=num_steps,
                            raster_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            polarimeter_mode="observe_polarimetric",
                            start_time=start_time + i * time_delta,
                        )
                        header = next(ds).header()
                        header["CAM__004"] = [0.02, 0.03][m % 2]
                        translated_header = translate_spec122_to_spec214_l0(header)
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
                        i += 1
            yield task
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


@pytest.fixture
def parse_task_with_multi_num_raster_steps(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task
):
    num_steps = 4
    num_map_scans = 2
    num_modstates = 2
    with ParseL0VispInputData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for map_scan in range(1, num_map_scans + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(num_steps):
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_raster_steps=num_steps,
                            raster_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            polarimeter_mode="observe_polarimetric",
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        translated_header["VSPNSTP"] = s % 3
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
            yield task
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


@pytest.fixture
def parse_task_with_incomplete_raster_scan(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task
):
    num_steps = 4
    num_maps = 2
    num_modstates = 2
    with ParseL0VispInputData(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for map_scan in range(1, num_maps + 1):
                for m in range(1, num_modstates + 1):
                    for s in range(num_steps):
                        ds = VispHeadersValidObserveFrames(
                            dataset_shape=(2, 2, 2),
                            array_shape=(1, 2, 2),
                            time_delta=10,
                            num_raster_steps=num_steps,
                            raster_step=s,
                            num_modstates=num_modstates,
                            modstate=m,
                            polarimeter_mode="observe_polarimetric",
                        )
                        header = next(ds).header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        translated_header["VSPNSTP"] = num_steps + 10
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[Tag.input(), Tag.frame()])
            yield task
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


def test_parse_visp_input_data(parse_inputs_valid_task, mocker):
    """
    Given: A ParseVispInputData task
    When: Calling the task instance
    Then: All tagged files exist and individual task tags are applied
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    parse_inputs_valid_task()
    # Then
    translated_input_files = parse_inputs_valid_task.read(tags=[Tag.input(), Tag.frame()])
    for filepath in translated_input_files:
        assert filepath.exists()

    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("DARK")]))
    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("LAMP_GAIN")]))
    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("SOLAR_GAIN")]))
    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("POLCAL")]))
    assert list(parse_inputs_valid_task.read(tags=[Tag.input(), Tag.task("OBSERVE")]))


def test_parse_visp_input_data_constants(parse_inputs_valid_task, mocker):
    """
    Given: A ParseVispInputData task
    When: Calling the task instance
    Then: Constants are in the constants object as expected
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    parse_inputs_valid_task()
    # Then
    assert parse_inputs_valid_task.constants._db_dict["NUM_MODSTATES"] == 2
    assert parse_inputs_valid_task.constants._db_dict["NUM_MAP_SCANS"] == 1
    assert parse_inputs_valid_task.constants._db_dict["NUM_RASTER_STEPS"] == 3
    assert parse_inputs_valid_task.constants._db_dict["WAVELENGTH"] == 656.28
    assert parse_inputs_valid_task.constants._db_dict["SPECTRAL_LINE"] == "VISP H alpha"
    assert parse_inputs_valid_task.constants._db_dict["DARK_EXPOSURE_TIMES"] == [1.0]
    assert parse_inputs_valid_task.constants._db_dict["LAMP_EXPOSURE_TIMES"] == [10.0]
    assert parse_inputs_valid_task.constants._db_dict["SOLAR_EXPOSURE_TIMES"] == [20.0]
    assert parse_inputs_valid_task.constants._db_dict["POLCAL_EXPOSURE_TIMES"] == [0.01]
    assert parse_inputs_valid_task.constants._db_dict["OBSERVE_EXPOSURE_TIMES"] == [0.02, 0.03]


def test_parse_visp_values(parse_inputs_valid_task, mocker):
    """
    :Given: A valid parse input task
    :When: Calling the task instance
    :Then: Values are correctly loaded into the constants mutable mapping
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    parse_inputs_valid_task()
    assert parse_inputs_valid_task.constants.instrument == "VISP"
    assert parse_inputs_valid_task.constants.average_cadence == 10
    assert parse_inputs_valid_task.constants.maximum_cadence == 10
    assert parse_inputs_valid_task.constants.minimum_cadence == 10
    assert parse_inputs_valid_task.constants.variance_cadence == 0


def test_multiple_num_raster_steps_raises_error(parse_task_with_multi_num_raster_steps, mocker):
    """
    :Given: A prase task with data that have inconsistent VSPNSTP values
    :When: Calling the parse task
    :Then: The correct error is raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    with pytest.raises(ValueError, match="Multiple NUM_RASTER_STEPS values found"):
        parse_task_with_multi_num_raster_steps()


def test_incomplete_raster_raises_error(parse_task_with_incomplete_raster_scan, mocker):
    """
    :Given: A prase task with data that has an incomplete raster scan
    :When: Calling the parse task
    :Then: The correct error is raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    with pytest.raises(ValueError, match="Did not find the correct set of raster step values"):
        parse_task_with_incomplete_raster_scan()
