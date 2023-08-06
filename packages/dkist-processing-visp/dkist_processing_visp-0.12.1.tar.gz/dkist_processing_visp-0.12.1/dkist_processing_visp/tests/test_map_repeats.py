import random
import re
from collections import defaultdict
from typing import List

import numpy as np
import pytest
from astropy.io import fits
from astropy.time import Time
from astropy.time import TimeDelta
from dkist_header_validator.translator import translate_spec122_to_spec214_l0
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)

from dkist_processing_visp.models.constants import VispBudName
from dkist_processing_visp.models.tags import VispStemName
from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.map_repeats import MapScanFlower
from dkist_processing_visp.parsers.map_repeats import NumMapScansBud
from dkist_processing_visp.parsers.map_repeats import PickyMapBud
from dkist_processing_visp.parsers.map_repeats import SingleScanStep
from dkist_processing_visp.parsers.raster_step import RasterScanStepFlower
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess
from dkist_processing_visp.tasks.parse import ParseL0VispInputData
from dkist_processing_visp.tasks.parse import S
from dkist_processing_visp.tests.conftest import VispHeadersValidObserveFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters


@pytest.fixture(scope="session")
def complete_map_headers():
    num_steps = 5
    num_modstates = 4
    num_maps = 3
    start_time = Time("1946-11-20T12:00:00")
    dt = TimeDelta(10, format="sec")
    i = 0
    header_list = []
    map_number_list = []
    for map_scan in range(1, num_maps + 1):
        for step_num in range(0, num_steps):
            for modstate in range(1, num_modstates + 1):
                ds = VispHeadersValidObserveFrames(
                    dataset_shape=(1, 2, 2),
                    array_shape=(1, 2, 2),
                    time_delta=10,
                    num_raster_steps=num_steps,
                    raster_step=step_num,
                    num_modstates=num_modstates,
                    modstate=modstate,
                    start_time=(start_time + i * dt).to_datetime(),
                )
                header = translate_spec122_to_spec214_l0(next(ds).header())
                header_list.append(header)
                map_number_list.append(map_scan)
                i += 1

    return header_list, num_steps, num_modstates, num_maps


@pytest.fixture(scope="session")
def map_headers_with_missing_steps():
    num_steps = 2
    num_modstates = 2
    num_maps = 3
    start_time = Time("1946-11-20T12:00:00")
    dt = TimeDelta(10, format="sec")
    i = 0
    header_list = []
    map_number_list = []
    for map_scan in range(1, num_maps + 1):
        for step_num in range(0, num_steps):
            if step_num == 0 and map_scan == 1:
                continue
            for modstate in range(1, num_modstates + 1):
                ds = VispHeadersValidObserveFrames(
                    dataset_shape=(1, 2, 2),
                    array_shape=(1, 2, 2),
                    time_delta=10,
                    num_raster_steps=num_steps,
                    raster_step=step_num,
                    num_modstates=num_modstates,
                    modstate=modstate,
                    start_time=(start_time + i * dt).to_datetime(),
                )
                header = translate_spec122_to_spec214_l0(next(ds).header())
                header_list.append(header)
                map_number_list.append(map_scan)
                i += 1

    return header_list, num_steps, num_modstates, num_maps


@pytest.fixture()
def organized_fits_access_dict(complete_map_headers):
    all_dict = defaultdict(lambda: defaultdict(list))

    for header in complete_map_headers[0]:
        fits_obj = VispL0FitsAccess.from_header(header)
        all_dict[fits_obj.raster_scan_step][fits_obj.modulator_state].append(fits_obj)

    return all_dict


class ParseTaskJustMapStuff(ParseL0VispInputData):
    @property
    def constant_flowers(self) -> List[S]:
        return [NumMapScansBud(), PickyMapBud()]

    @property
    def tag_flowers(self) -> List[S]:
        return [
            MapScanFlower(),
            RasterScanStepFlower(),
            SingleValueSingleKeyFlower(
                tag_stem_name=VispStemName.modstate.value, metadata_key="modulator_state"
            ),
        ]


@pytest.fixture()
def map_only_parse_task_with_correct_map(
    complete_map_headers, tmp_path_factory, recipe_run_id, assign_input_dataset_doc_to_task
):

    complete_headers, num_steps, num_modstates, num_maps = complete_map_headers
    with ParseTaskJustMapStuff(
        recipe_run_id=recipe_run_id, workflow_name="parse_map_scans", workflow_version="X.Y.Z"
    ) as task:
        try:
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path_factory.mktemp("map_scan"), recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for header in complete_headers:
                hdu = fits.PrimaryHDU(data=np.ones((1, 2, 2)), header=fits.Header(header))
                hdul = fits.HDUList([hdu])
                task.fits_data_write(hdu_list=hdul, tags=[VispTag.input(), VispTag.frame()])

            yield task, num_steps, num_modstates, num_maps
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


@pytest.fixture()
def map_only_parse_task_with_missing_steps(
    map_headers_with_missing_steps,
    tmp_path_factory,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
):

    complete_headers, num_steps, num_modstates, num_maps = map_headers_with_missing_steps
    with ParseTaskJustMapStuff(
        recipe_run_id=recipe_run_id, workflow_name="parse_map_scans", workflow_version="X.Y.Z"
    ) as task:
        try:
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path_factory.mktemp("map_scan"), recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for header in complete_headers:
                hdu = fits.PrimaryHDU(data=np.ones((1, 2, 2)), header=fits.Header(header))
                hdul = fits.HDUList([hdu])
                task.fits_data_write(hdu_list=hdul, tags=[VispTag.input(), VispTag.frame()])

            yield task, num_steps, num_modstates, num_maps
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


@pytest.fixture
def map_only_parse_task_with_multiple_exposures_per_raster_step(
    tmp_path, recipe_run_id, assign_input_dataset_doc_to_task
):
    num_steps = 4
    num_exp = 3
    num_modstates = 2
    start_time = Time("1946-11-20T12:00:00")
    dt = TimeDelta(10, format="sec")
    i = 0
    with ParseTaskJustMapStuff(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task._scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispTestingParameters())
            for s in range(num_steps):
                for m in range(1, num_modstates + 1):
                    ds = VispHeadersValidObserveFrames(
                        dataset_shape=(num_exp, 2, 2),
                        array_shape=(1, 2, 2),
                        time_delta=0,  # This is where we produce multiple exposures
                        num_raster_steps=num_steps,
                        raster_step=s,
                        num_modstates=num_modstates,
                        modstate=m,
                        polarimeter_mode="observe_polarimetric",
                        start_time=(start_time + i * dt).to_datetime(),
                    )
                    for d in ds:
                        header = d.header()
                        translated_header = translate_spec122_to_spec214_l0(header)
                        hdu = fits.PrimaryHDU(
                            data=np.ones((1, 2, 2)), header=fits.Header(translated_header)
                        )
                        hdul = fits.HDUList([hdu])
                        task.fits_data_write(hdu_list=hdul, tags=[VispTag.input(), VispTag.frame()])
                    i += 1
            yield task, num_exp
        except:
            raise
        finally:
            task.scratch.purge()
            task.constants._purge()


def test_singlescanstep_correct(organized_fits_access_dict):
    """
    :Given: A group of FitsAccess objects corresponding to multiple map scans with unique frames
    :When: Using the SingleScanStep object to distill the FitsAccess objects
    :Then: The resulting objects sort correctly and are not equal to each other
    """
    # Test sorting happens correctly
    for modstate_dict in organized_fits_access_dict.values():
        for access_list in modstate_dict.values():
            singlescan_list = [SingleScanStep(o) for o in access_list]
            random.shuffle(singlescan_list)  # Put them out of order
            obj_sort_idx = np.argsort(singlescan_list)
            time_sort_idx = np.argsort([s.date_obs for s in singlescan_list])
            assert np.array_equal(obj_sort_idx, time_sort_idx)

    # Test that the first object from each (raster_step, modstate, date_obs) tuple is unequal to all others
    flat_obj_list = sum(
        sum([list(md.values()) for md in organized_fits_access_dict.values()], []), []
    )
    # I.e., the entire set of values is identical to the unique set of values
    assert len(set(flat_obj_list)) == len(flat_obj_list)


def test_parse_map_repeats(map_only_parse_task_with_correct_map):
    """
    :Given: A map-parsing task with files that represent complete maps
    :When: Parsing the files
    :Then: The correct number of map scans is inferred and each file is tagged correctly
    """
    task, num_steps, num_modstates, num_maps = map_only_parse_task_with_correct_map
    task()

    assert task.constants._db_dict[VispBudName.num_map_scans.value] == num_maps
    for step in range(0, num_steps):
        for modstate in range(1, num_modstates + 1):
            files = list(
                task.read(
                    tags=[
                        VispTag.input(),
                        VispTag.frame(),
                        VispTag.raster_step(step),
                        VispTag.modstate(modstate),
                    ]
                )
            )
            assert len(files) == num_maps
            map_scan_tags = [
                [
                    t.replace(f"{VispStemName.map_scan.value}_", "")
                    for t in task.tags(f)
                    if VispStemName.map_scan.value in t
                ][0]
                for f in files
            ]
            time_list = [Time(VispL0FitsAccess.from_path(f).time_obs) for f in files]
            map_idx = np.argsort(map_scan_tags)
            time_idx = np.argsort(time_list)
            assert np.array_equal(time_idx, map_idx)


def test_missing_map_raises_error(map_only_parse_task_with_missing_steps):
    """
    :Given: A map-parsing task with files corresponding to a set of maps where one map is missing a step
    :When: Parsing the files
    :Then: The correct error is raised
    """
    task, num_steps, num_modstates, num_maps = map_only_parse_task_with_missing_steps
    expected_num_frames = num_steps * num_modstates

    with pytest.raises(
        ValueError,
        match=re.escape(
            f"All maps do not have the same number of frames. Set of num frames is { {expected_num_frames, expected_num_frames - num_modstates} }"
        ),
    ):
        task()


def test_multiple_exp_per_step_raises_error(
    map_only_parse_task_with_multiple_exposures_per_raster_step,
):
    """
    :Given: A map-parsing task with data that has multiple exposures per (raster, modstate, map_scan)
    :When: Calling the parse task
    :Then: The correct error is raised
    """
    task, num_exp = map_only_parse_task_with_multiple_exposures_per_raster_step
    with pytest.raises(
        ValueError,
        match=re.escape(
            f"More than one exposure detected for a single map scan of a single map step. (Randomly chosen step has {num_exp} exposures)."
        ),
    ):
        task()
