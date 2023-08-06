"""Visp dark task."""
import logging

from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_processing_math.statistics import average_numpy_arrays

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.mixin.input_frame_loaders import InputFrameLoadersMixin
from dkist_processing_visp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_visp.tasks.visp_base import VispTaskBase


class DarkCalibration(
    VispTaskBase, InputFrameLoadersMixin, IntermediateFrameHelpersMixin, QualityMixin
):
    """
    Task class for calculation of the averaged dark frame for a VISP calibration run.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs



    """

    record_provenance = True

    def run(self):
        """
        For each beam.

            - Gather input dark frames
            - Calculate master dark
            - Write master dark
            - Record quality metrics

        Returns
        -------
        None

        """
        target_exp_times = list(
            set(
                self.constants.solar_exposure_times
                + self.constants.observe_exposure_times
                + self.constants.polcal_exposure_times
                + self.constants.lamp_exposure_times
            )
        )
        logging.info(f"{target_exp_times = }")
        with self.apm_task_step(
            f"Calculating dark frames for {self.constants.num_beams} beams and {len(target_exp_times)} exp times"
        ):
            total_dark_frames_used = 0
            for exp_time in target_exp_times:
                for beam in range(1, self.constants.num_beams + 1):
                    logging.info(f"Gathering input dark frames for {exp_time = } and {beam = }")
                    dark_tags = [
                        VispTag.input(),
                        VispTag.frame(),
                        VispTag.task("DARK"),
                        VispTag.exposure_time(exp_time),
                    ]
                    current_exp_dark_count = self.scratch.count_all(tags=dark_tags)
                    if current_exp_dark_count == 0:
                        raise ValueError(f"Could not find any darks for {exp_time = }")
                    total_dark_frames_used += current_exp_dark_count
                    input_dark_arrays = self.input_frame_loaders_dark_array_generator(
                        beam=beam, exposure_time=exp_time
                    )

                    with self.apm_processing_step(
                        f"Calculating dark for {exp_time = } and {beam = }"
                    ):
                        logging.info(f"Calculating dark for {exp_time = } and {beam = }")
                        averaged_dark_array = average_numpy_arrays(input_dark_arrays)

                    with self.apm_writing_step(f"Writing dark for {exp_time = } {beam = }"):
                        logging.info(f"Writing dark for {exp_time = } {beam = }")
                        self.intermediate_frame_helpers_write_arrays(
                            averaged_dark_array,
                            beam=beam,
                            task="DARK",
                            exposure_time=exp_time,
                        )

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_dark_frames: int = self.scratch.count_all(
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("DARK"),
                ],
            )
            unused_count = int(no_of_raw_dark_frames - (total_dark_frames_used / 2))
            self.quality_store_task_type_counts(
                task_type="dark", total_frames=no_of_raw_dark_frames, frames_not_used=unused_count
            )
