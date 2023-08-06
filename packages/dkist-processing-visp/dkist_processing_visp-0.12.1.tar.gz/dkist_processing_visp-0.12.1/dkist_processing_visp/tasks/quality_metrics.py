"""ViSP quality metrics task."""
from dataclasses import dataclass
from dataclasses import field
from typing import List

import numpy as np
from astropy.time import Time
from dkist_processing_common.parsers.quality import L1QualityFitsAccess
from dkist_processing_common.tasks import QualityL0Metrics
from dkist_processing_common.tasks.mixin.quality import QualityMixin

from dkist_processing_visp.models.constants import VispConstants
from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.visp_base import VispTaskBase


@dataclass
class _QualityData:
    """Class for storage of Visp quality data."""

    datetimes: List[str] = field(default_factory=list)
    Q_RMS_noise: List[float] = field(default_factory=list)
    U_RMS_noise: List[float] = field(default_factory=list)
    V_RMS_noise: List[float] = field(default_factory=list)
    intensity_values: List[float] = field(default_factory=list)


@dataclass
class _QualityTaskTypeData:
    """Class for storage of Visp quality task type data."""

    quality_task_type: str
    average_values: List[float] = field(default_factory=list)
    rms_values_across_frame: List[float] = field(default_factory=list)
    datetimes: List[str] = field(default_factory=list)

    @property
    def has_values(self) -> bool:
        return bool(self.average_values)


class VispL0QualityMetrics(QualityL0Metrics):
    """
    Task class for collection of Visp L0 specific quality metrics.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    def constants_model_class(self):
        """Class for Visp constants."""
        return VispConstants

    def run(self) -> None:
        """Calculate L0 metrics for ViSP data."""
        if not self.constants.correct_for_polarization:
            paths = self.read(tags=[VispTag.input()])
            self.calculate_l0_metrics(paths=paths)
        else:
            for m in range(1, self.constants.num_modstates + 1):
                with self.apm_task_step(f"Working on modstate {m}"):
                    paths = self.read(tags=[VispTag.input(), VispTag.modstate(m)])
                    self.calculate_l0_metrics(paths=paths, modstate=m)


class VispL1QualityMetrics(VispTaskBase, QualityMixin):
    """
    Task class for collection of Visp L1 specific quality metrics.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    def run(self) -> None:
        """
        For each spectral scan.

            - Gather stokes data
            - Find Stokes Q, U, and V RMS noise
            - Find the polarimetric sensitivity (smallest intensity signal measured)
            - Send metrics for storage

        """
        if self.constants.correct_for_polarization:
            self.compute_polarimetric_metrics()

        self.compute_noise()

    def compute_polarimetric_metrics(self) -> None:
        """Compute RMS noise and sensitivity estimate for L1 Visp frames."""
        with self.apm_processing_step("Calculating polarization metrics"):
            all_datetimes = []
            all_Q_RMS_noise = []
            all_U_RMS_noise = []
            all_V_RMS_noise = []
            all_pol_sens_values = []
            for map_scan in range(1, self.constants.num_map_scans + 1):
                polarization_data = _QualityData()
                for step in range(0, self.constants.num_raster_steps):

                    # grab stokes I data
                    stokesI_frame = next(
                        self.fits_data_read_fits_access(
                            tags=[
                                VispTag.output(),
                                VispTag.frame(),
                                VispTag.raster_step(step),
                                VispTag.map_scan(map_scan),
                                VispTag.stokes("I"),
                            ],
                            cls=L1QualityFitsAccess,
                        )
                    )
                    stokesI_data = stokesI_frame.data
                    polarization_data.datetimes.append(Time(stokesI_frame.time_obs).mjd)
                    polarization_data.intensity_values.append(np.max(stokesI_data))

                    # grab other stokes data and find and store RMS noise
                    for stokes_param, data_list in zip(
                        ("Q", "U", "V"),
                        (
                            polarization_data.Q_RMS_noise,
                            polarization_data.U_RMS_noise,
                            polarization_data.V_RMS_noise,
                        ),
                    ):
                        stokes_frame = next(
                            self.fits_data_read_fits_access(
                                tags=[
                                    VispTag.output(),
                                    VispTag.frame(),
                                    VispTag.raster_step(step),
                                    VispTag.map_scan(map_scan),
                                    VispTag.stokes(stokes_param),
                                ],
                                cls=L1QualityFitsAccess,
                            )
                        )
                        # find Stokes RMS noise
                        data_list.append(np.std(stokes_frame.data / stokesI_data))

                all_datetimes.append(Time(np.mean(polarization_data.datetimes), format="mjd").isot)
                all_Q_RMS_noise.append(np.average(polarization_data.Q_RMS_noise))
                all_U_RMS_noise.append(np.average(polarization_data.U_RMS_noise))
                all_V_RMS_noise.append(np.average(polarization_data.V_RMS_noise))
                # find the polarimetric sensitivity of this map_scan (smallest intensity signal measured)
                polarimetric_sensitivity = 1 / np.max(polarization_data.intensity_values)
                all_pol_sens_values.append(polarimetric_sensitivity)

        with self.apm_step("Sending lists for storage"):
            for stokes_index, stokes_noise in zip(
                ("Q", "U", "V"), (all_Q_RMS_noise, all_U_RMS_noise, all_V_RMS_noise)
            ):
                self.quality_store_polarimetric_noise(
                    stokes=stokes_index, datetimes=all_datetimes, values=stokes_noise
                )
            self.quality_store_polarimetric_sensitivity(
                datetimes=all_datetimes, values=all_pol_sens_values
            )

    def compute_noise(self):
        """Compute noise in data."""
        with self.apm_processing_step("Calculating L1 ViSP noise metrics"):
            for stokes in ["I", "Q", "U", "V"]:
                tags = [VispTag.output(), VispTag.frame(), VispTag.stokes(stokes)]
                if self.scratch.count_all(tags=tags) > 0:
                    frames = self.fits_data_read_fits_access(
                        tags=tags,
                        cls=L1QualityFitsAccess,
                    )
                    noise_values = []
                    datetimes = []
                    for frame in frames:
                        noise_values.append(self.avg_noise(frame.data))
                        datetimes.append(frame.time_obs)
                    self.quality_store_noise(
                        datetimes=datetimes, values=noise_values, stokes=stokes
                    )
