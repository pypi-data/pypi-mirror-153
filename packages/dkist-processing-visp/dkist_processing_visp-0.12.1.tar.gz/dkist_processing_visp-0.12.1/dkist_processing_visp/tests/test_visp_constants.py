from dataclasses import asdict
from dataclasses import dataclass
from typing import Tuple

import pytest

from dkist_processing_visp.tasks.visp_base import VispTaskBase


@dataclass
class testing_constants:
    num_modstates: int = 10
    num_beams: int = 2
    num_cs_steps: int = 18
    num_raster_steps: int = 1000
    polarimeter_mode: str = "observe_polarimetric"
    wavelength: float = 666.6
    lamp_exposure_times: Tuple[float] = (100.0,)
    solar_exposure_times: Tuple[float] = (1.0,)
    observe_exposure_times: Tuple[float] = (0.01,)
    # We don't need all the common ones, but let's put one just to check
    instrument: str = "CHECK_OUT_THIS_INSTRUMENT"


@pytest.fixture(scope="session")
def expected_constant_dict() -> dict:
    lower_dict = asdict(testing_constants())
    return {k.upper(): v for k, v in lower_dict.items()}


@pytest.fixture(scope="function")
def visp_science_task_with_constants(recipe_run_id, expected_constant_dict, init_visp_constants_db):
    class Task(VispTaskBase):
        def run(self):
            ...

    init_visp_constants_db(recipe_run_id, expected_constant_dict)
    task = Task(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_visp_input_data",
        workflow_version="VX.Y",
    )

    yield task

    task.constants._purge()


def test_visp_constants(visp_science_task_with_constants, expected_constant_dict):

    task = visp_science_task_with_constants
    for k, v in expected_constant_dict.items():
        if type(v) is tuple:
            v = list(v)
        if k == "POLARIMETER_MODE":
            continue
        assert getattr(task.constants, k.lower()) == v
    assert task.constants.correct_for_polarization == True
