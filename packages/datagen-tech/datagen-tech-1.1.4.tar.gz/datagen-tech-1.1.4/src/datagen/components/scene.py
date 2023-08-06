from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from datagen.components.camera import Camera
from datagen.components.datapoint import DataPoint


@dataclass
class Scene:
    path: Path
    cameras: List[Camera] = field(init=False, repr=False)

    def __post_init__(self):
        self.cameras = self._init_cameras()

    def _init_cameras(self) -> List[Camera]:
        return [Camera(name=camera_name, scene_path=self.path) for camera_name in self._get_cameras_names()]

    def _get_cameras_names(self) -> List[str]:
        return list(set(cam_dir.name for cam_dir in self.path.rglob("*camera*") if cam_dir.is_dir()))

    @property
    def datapoints(self) -> List[DataPoint]:
        return [datapoint for datapoint in self]

    def __getitem__(self, key):
        return self.datapoints[key]

    def __iter__(self):
        for camera in self.cameras:
            for datapoint in camera:
                yield datapoint

    def __len__(self):
        return len(self.datapoints)
