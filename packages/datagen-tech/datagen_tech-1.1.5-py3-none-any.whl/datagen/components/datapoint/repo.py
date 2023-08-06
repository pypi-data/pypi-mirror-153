from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterable

from dependency_injector import containers
from dependency_injector.wiring import inject

from datagen.components.datapoint import DataPoint

SINGLE_FRAME_RANGE = range(1)


@inject
@dataclass
class DatapointsRepository:
    datapoints_container: containers.DeclarativeContainer

    def get_datapoints(self, scene_path: Path, camera_name: str) -> List[DataPoint]:
        datapoints = []
        for frame_num in self._get_frames_range(scene_path):
            for environment in self._get_environments(scene_path, camera_name, frame_num):
                datapoints.append(
                    self.datapoints_container.factory(
                        scene_path=scene_path,
                        camera=camera_name,
                        frame_num=frame_num,
                        visible_spectrum_image=environment.image_name,
                    )
                )
        return datapoints

    def _get_frames_range(self, scene_path: Path) -> range:
        scene_frames_path = scene_path.joinpath("frames")
        if scene_frames_path.exists():
            return self._get_multiple_frames_range(scene_frames_path)
        else:
            return SINGLE_FRAME_RANGE

    @staticmethod
    def _get_multiple_frames_range(scene_frames_path: Path) -> range:
        frames_num = len(list(scene_frames_path.iterdir()))
        return range(1, frames_num + 1)

    def _get_environments(self, scene_path: Path, camera_name: str, frame_num: int) -> Iterable:
        environments_file_path = self._get_environments_file_path(scene_path, camera_name, frame_num)
        return self.datapoints_container.modalities().read_textual_modality(
            modality_factory_name="environments", modality_file_path=environments_file_path
        )

    @staticmethod
    def _get_environments_file_path(scene_path: Path, camera_name: str, frame_num: int) -> str:
        if frame_num > 0:
            environments_file_path = scene_path.joinpath(
                "frames", str(frame_num).zfill(3), camera_name, "environment.json"
            )
        else:
            environments_file_path = scene_path.joinpath(camera_name, "environment.json")
        return str(environments_file_path)
