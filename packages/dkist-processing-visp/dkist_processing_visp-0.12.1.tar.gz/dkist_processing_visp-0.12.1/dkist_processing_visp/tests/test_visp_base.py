import numpy as np
import pytest
from astropy.io import fits
from dkist_processing_common._util.scratch import WorkflowFileSystem

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_visp.tasks.visp_base import VispTaskBase
from dkist_processing_visp.tests.conftest import VispConstantsDb
from dkist_processing_visp.tests.conftest import VispTestingParameters

NUM_BEAMS = 2
NUM_MODSTATES = 8
NUM_CS_STEPS = 6
NUM_RASTER_STEPS = 10
WAVE = 666.0


@pytest.fixture(scope="function")
def visp_science_task(recipe_run_id, assign_input_dataset_doc_to_task, init_visp_constants_db):
    class Task(VispTaskBase, IntermediateFrameHelpersMixin):
        def run(self):
            ...

    constants_db = VispConstantsDb(
        NUM_MODSTATES=NUM_MODSTATES,
        NUM_CS_STEPS=NUM_CS_STEPS,
        NUM_RASTER_STEPS=NUM_RASTER_STEPS,
        WAVELENGTH=WAVE,
        POLARIMETER_MODE="observe_polarimetric",
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    task = Task(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    )
    assign_input_dataset_doc_to_task(task, VispTestingParameters())

    yield task

    task.constants._purge()


def test_write_intermediate_arrays(visp_science_task):
    """
    Given: A VispTaskBase task
    When: Using the helper to write a single intermediate array
    Then: The array is written and tagged correctly
    """
    data = np.random.random((10, 10))
    head = fits.Header()
    head["TEST"] = "foo"
    visp_science_task.intermediate_frame_helpers_write_arrays(
        arrays=data, headers=head, beam=1, map_scan=2, raster_step=3, task="BAR"
    )
    loaded_list = list(
        visp_science_task.fits_data_read_hdu(
            tags=[
                VispTag.intermediate(),
                VispTag.frame(),
                VispTag.beam(1),
                VispTag.map_scan(2),
                VispTag.raster_step(3),
                VispTag.task("BAR"),
            ]
        )
    )
    assert len(loaded_list) == 1
    hdu = loaded_list[0][1]
    np.testing.assert_equal(hdu.data, data)
    assert hdu.header["TEST"] == "foo"


def test_write_intermediate_arrays_none_header(visp_science_task):
    """
    Given: A VispTaskBase task
    When: Using the helper to write a single intermediate array with no header
    Then: The array is written and tagged correctly
    """
    data = np.random.random((10, 10))
    visp_science_task.intermediate_frame_helpers_write_arrays(
        arrays=data, headers=None, beam=1, map_scan=2, raster_step=3, task="BAR"
    )
    loaded_list = list(
        visp_science_task.fits_data_read_hdu(
            tags=[
                VispTag.intermediate(),
                VispTag.frame(),
                VispTag.beam(1),
                VispTag.map_scan(2),
                VispTag.raster_step(3),
                VispTag.task("BAR"),
            ]
        )
    )
    assert len(loaded_list) == 1
    hdu = loaded_list[0][1]
    np.testing.assert_equal(hdu.data, data)


@pytest.fixture
def visp_science_task_with_tagged_intermediates(
    recipe_run_id, tmpdir_factory, init_visp_constants_db
):
    class Task(VispTaskBase, IntermediateFrameHelpersMixin):
        def run(self):
            ...

    init_visp_constants_db(recipe_run_id, VispConstantsDb())
    task = Task(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    )
    task._scratch = WorkflowFileSystem(scratch_base_path=tmpdir_factory.mktemp("data"))
    tag_names = [["beam"], ["exposure_time", "task"], ["modstate"]]
    tag_vals = [[1], [10.23, "dark"], [3]]
    tag_fcns = [[getattr(VispTag, n) for n in nl] for nl in tag_names]
    tag_list = [[f(v) for f, v in zip(fl, vl)] for fl, vl in zip(tag_fcns, tag_vals)]
    for i, tags in enumerate(tag_list):
        hdul = fits.HDUList([fits.PrimaryHDU(data=np.ones((2, 2)) * i)])
        fname = task.scratch.workflow_base_path / f"file{i}.fits"
        hdul.writeto(fname)
        task.tag(fname, tags + [VispTag.intermediate(), VispTag.frame()])

    yield task, tag_names, tag_vals

    task.constants._purge()
    task.scratch.purge()


def test_load_intermediate_arrays(visp_science_task_with_tagged_intermediates):

    task, tag_names, tag_vals = visp_science_task_with_tagged_intermediates
    kwarg_list = [{k: v for k, v in zip(kl, vl)} for kl, vl in zip(tag_names, tag_vals)]
    for i, kwargs in enumerate(kwarg_list):
        arrays = list(task.intermediate_frame_helpers_load_intermediate_arrays(**kwargs))
        assert len(arrays) == 1
        np.testing.assert_equal(arrays[0], np.ones((2, 2)) * i)


def test_load_intermediate_dark_array():
    pass


def test_load_intermediate_lamp_gain_array():
    pass


def test_load_intermediate_solar_gain_array():
    pass


def test_load_intermediate_geometric_hdu_list():
    pass


def test_load_intermediate_demodulated_arrays():
    pass
