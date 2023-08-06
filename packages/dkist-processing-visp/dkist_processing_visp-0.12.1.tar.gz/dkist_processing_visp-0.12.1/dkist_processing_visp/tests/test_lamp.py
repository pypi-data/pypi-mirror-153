import json
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.lamp import LampCalibration
from dkist_processing_visp.tests.conftest import FakeGQLClient
from dkist_processing_visp.tests.conftest import generate_fits_frame
from dkist_processing_visp.tests.conftest import VispConstantsDb
from dkist_processing_visp.tests.conftest import VispHeadersValidLampGainFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters

RNG = np.random.default_rng()


@dataclass
class VispLampTestingParameters(VispTestingParameters):
    visp_beam_border: int = 10


@pytest.fixture(scope="function")
def lamp_calibration_task(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db, mocker
):
    number_of_modstates = 2
    number_of_beams = 2
    exposure_time = 10.0  # From VispHeadersValidLampGainFrames fixture
    dataset_shape = (number_of_modstates, 20, 10)
    array_shape = (1, 20, 10)
    intermediate_shape = (10, 10)
    constants_db = VispConstantsDb(
        NUM_MODSTATES=number_of_modstates, LAMP_EXPOSURE_TIMES=(exposure_time,)
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with LampCalibration(
        recipe_run_id=recipe_run_id, workflow_name="lamp_gain_calibration", workflow_version="VX.Y"
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispLampTestingParameters())
            beam_border = task.parameters.beam_border
            dark_signal = 3.0
            start_time = datetime.now()
            # Make intermediate dark frame
            dark_cal = np.ones(intermediate_shape) * dark_signal
            dark_hdul = fits.HDUList([fits.PrimaryHDU(data=dark_cal)])
            # Need a dark for each beam
            for b in range(number_of_beams):
                task.intermediate_frame_helpers_write_arrays(
                    arrays=dark_cal, beam=b + 1, task="DARK", exposure_time=exposure_time
                )
            # These images are for two combined beams
            for i in range(number_of_modstates):
                ds = VispHeadersValidLampGainFrames(
                    dataset_shape=dataset_shape,
                    array_shape=array_shape,
                    time_delta=10,
                    num_modstates=number_of_modstates,
                    modstate=i + 1,
                    start_time=start_time,
                )
                header_generator = (
                    spec122_validator.validate_and_translate_to_214_l0(
                        d.header(), return_type=fits.HDUList
                    )[0].header
                    for d in ds
                )
                hdul = generate_fits_frame(header_generator=header_generator, shape=array_shape)
                # Tweak data so that beam sides are slightly different
                # Use data != 1 to check normalization in test
                hdul[0].data[0, :beam_border, :] = 1.1
                hdul[0].data[0, beam_border:, :] = 1.2
                task.fits_data_write(
                    hdu_list=hdul,
                    tags=[
                        VispTag.input(),
                        VispTag.task("LAMP_GAIN"),
                        VispTag.modstate(i + 1),
                        VispTag.frame(),
                        VispTag.exposure_time(exposure_time),
                    ],
                )
            yield task, number_of_modstates, number_of_beams
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


def test_lamp_calibration_task(lamp_calibration_task, mocker):
    """
    Given: A LampCalibration task
    When: Calling the task instance
    Then: The correct number of output lamp gain frames exists, and are tagged correctly
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task, number_of_modstates, number_of_beams = lamp_calibration_task
    task()
    # Then
    tags = [
        VispTag.task("LAMP_GAIN"),
        VispTag.intermediate(),
    ]
    assert len(list(task.read(tags=tags))) == number_of_modstates * number_of_beams

    for i in range(number_of_modstates):
        for j in range(number_of_beams):
            tags = [
                VispTag.task("LAMP_GAIN"),
                VispTag.intermediate(),
                VispTag.modstate(i + 1),
                VispTag.beam(j + 1),
            ]
            files = list(task.read(tags=tags))
            assert len(files) == 1
            hdu = fits.open(files[0])[0]
            np.testing.assert_allclose(hdu.data, np.ones((10, 10)))  # Because lamps are normalized

    tags = [
        VispTag.task("LAMP_GAIN"),
        VispTag.intermediate(),
    ]
    for filepath in task.read(tags=tags):
        assert filepath.exists()

    quality_files = task.read(tags=[Tag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[VispTag.input(), VispTag.frame(), VispTag.task("LAMP_GAIN")]
            )
