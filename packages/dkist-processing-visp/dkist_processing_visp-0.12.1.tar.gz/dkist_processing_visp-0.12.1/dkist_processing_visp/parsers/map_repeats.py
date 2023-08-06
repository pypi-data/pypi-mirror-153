"""Stems for organizing files into separate map scans."""
from __future__ import annotations

from abc import ABC
from collections import defaultdict
from functools import cached_property
from typing import Dict
from typing import List
from typing import Type
from typing import Union

from astropy.time import Time
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.flower_pot import Thorn

from dkist_processing_visp.models.constants import VispBudName
from dkist_processing_visp.models.tags import VispStemName
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


class SingleScanStep:
    """
    An object that uniquely defines a (raster_step, modstate, time_obs) tuple from any number of map scan repeates.

    This is just a fancy tuple.

    Basically, it just hashes the (raster_step, modstate, time_obs) tuple so these objects can easily be compared.
    Also uses the time_obs property so that multiple map scan repeats of the same (step, modstate) can be sorted.

    This is just a fancy tuple.
    """

    def __init__(self, fits_obj: VispL0FitsAccess):
        """Read raster step, modstate, and obs time information from a FitsAccess object."""
        self.raster_step = fits_obj.raster_scan_step
        self.modulator_state = fits_obj.modulator_state
        self.date_obs = Time(fits_obj.time_obs)

    def __repr__(self):
        return f"SingleScanStep with {self.raster_step = }, {self.modulator_state = }, and {self.date_obs = }"

    def __eq__(self, other: SingleScanStep) -> bool:
        """Two frames are equal if they have the same (raster_step, modstate) tuple."""
        if not isinstance(other, SingleScanStep):
            raise TypeError(f"Cannon compare MapRepeat with type {type(other)}")

        for attr in ["raster_step", "modulator_state", "date_obs"]:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def __lt__(self, other: SingleScanStep) -> bool:
        """Only sort on date_obs."""
        return self.date_obs < other.date_obs

    def __hash__(self) -> int:
        # Not strictly necessary, but does allow for using set() on these objects
        return hash((self.raster_step, self.modulator_state, self.date_obs))


class MapScanStemBase(Stem, ABC):
    """Base class for Stems that use a dictionary of [int, Dict[int, SingleScanStep]] to analyze map_scan-related stuff."""

    # This only here so type-hinting of this complex dictionary will work.
    key_to_petal_dict: Dict[str, SingleScanStep]

    @cached_property
    def scan_step_dict(self) -> Dict[int, Dict[int, List[SingleScanStep]]]:
        """Nested dictionary that contains a SingleScanStep for each ingested frame.

        Dictionary structure is [raster_step (int), Dict[modstate (int), List[SingleScanStep]]
        """
        scan_step_dict = defaultdict(lambda: defaultdict(list))
        for scan_step_obj in self.key_to_petal_dict.values():
            scan_step_dict[scan_step_obj.raster_step][scan_step_obj.modulator_state].append(
                scan_step_obj
            )

        return scan_step_dict

    def setter(self, fits_obj: VispL0FitsAccess) -> Union[SingleScanStep, Type[SpilledDirt]]:
        """Ingest observe frames as SingleScanStep objects."""
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt
        return SingleScanStep(fits_obj=fits_obj)


class MapScanFlower(MapScanStemBase):
    """Flower for computing and assigning map scan numbers."""

    def __init__(self):
        super().__init__(stem_name=VispStemName.map_scan.value)

    def getter(self, key: str) -> int:
        """Compute the map scan number for a single frame.

        The frame implies a SingleScanStep. That object is then compared to the sorted list of objects for a single
        (raster_step, modstate) tuple. The location within that sorted list is the map scan number.
        """
        scan_step_obj = self.key_to_petal_dict[key]
        step_list = sorted(
            self.scan_step_dict[scan_step_obj.raster_step][scan_step_obj.modulator_state]
        )
        num_exp = step_list.count(scan_step_obj)
        if num_exp > 1:
            raise ValueError(
                f"More than one exposure detected for a single map scan of a single map step. (Randomly chosen step has {num_exp} exposures)."
            )
        return step_list.index(scan_step_obj) + 1  # Here we decide that map scan indices start at 1


class NumMapScansBud(MapScanStemBase):
    """Bud for determining the total number of map scans.

    Also checks that all raster steps have the same number of map scans.
    """

    def __init__(self):
        super().__init__(stem_name=VispBudName.num_map_scans.value)

    def getter(self, key: str) -> int:
        """Compute the total number of map scans.

        This is simply the length of the lists associated with a single (raster_step, modstate) tuple.
        """
        unique_num_maps = set(
            sum([[len(m) for m in md.values()] for md in self.scan_step_dict.values()], [])
        )
        return unique_num_maps.pop()


class PickyMapBud(MapScanStemBase):
    """PickyBud for checking that:.

    1. All maps have the same number of frames
    2. All steps have the same number of modstates
    3. All maps have num_steps * num_modstates frames
    """

    def __init__(self):
        super().__init__(stem_name="PICKY_MAP_STUFF")

    def getter(self, key: str) -> Type[Thorn]:
        """Check constraints on how the maps are assembled."""
        map_scan_num_frames = defaultdict(int)
        num_steps = len(self.scan_step_dict)
        num_modstate_set = set()
        for raster_scan_step, modulator_states in self.scan_step_dict.items():
            num_modstate_set.add(len(modulator_states))
            for modulator_state, step_obj_list in modulator_states.items():
                sorted_steps = sorted(step_obj_list)
                for index, step_obj in enumerate(sorted_steps):
                    map_scan = index + 1  # map scans count from 1, not 0
                    map_scan_num_frames[map_scan] += 1

        if len(num_modstate_set) > 1:
            raise ValueError(
                f"All raster steps do not have the same number of modstates. Set of number of modstates is {num_modstate_set}"
            )

        num_modstates = num_modstate_set.pop()
        expected_num_frames = num_modstates * num_steps
        num_frames_set = set(map_scan_num_frames.values())
        if len(num_frames_set) > 1:
            raise ValueError(
                f"All maps do not have the same number of frames. Set of num frames is {num_frames_set}"
            )

        # It's very possible that this check will never fail if the above checks also pass.
        # This is because the num_modstates and num_steps are taken empirically from the found data,
        # NOT from header values. In other words, it might be true that if the previous two checks pass
        # then this check will pass tautologically.
        #
        # If you're looking for where the actual header values are used to make sure the set of data is consistent
        # then check out the `TotalRasterStepsBud` in raster_steps.py
        found_num_frames = num_frames_set.pop()
        if found_num_frames != expected_num_frames:
            raise ValueError(
                f"Expected to find {expected_num_frames} for all maps. Found {found_num_frames} instead."
            )

        return Thorn
