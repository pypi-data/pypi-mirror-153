from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterator

from datagen.components.scene import Scene

# Older datasets scenes are named "environment_XXXXX".
SCENE_FOLDER_NAME_PATTERNS = ["scene_*", "environment_*"]


class CorruptedSourceError(ValueError):
    ...


@dataclass
class DataSource:
    path: Path

    @property
    def environment(self) -> str:
        return "identities"

    def init_scenes(self) -> List[Scene]:
        scenes = [Scene(path=path_) for path_ in sorted(self.path.iterdir()) if self._is_path_to_scene(path_)]
        if len(scenes) == 0:
            raise CorruptedSourceError(f"Corrupted source: {str(self.path)}")
        return scenes

    @staticmethod
    def _is_path_to_scene(path: Path) -> bool:
        return any(path.match(pattern) for pattern in SCENE_FOLDER_NAME_PATTERNS) and path.is_dir()


@dataclass
class SourcesRepository:
    sources_paths: List[str]

    def get_all(self) -> Iterator[DataSource]:
        for path in self.sources_paths:
            yield DataSource(path=Path(path))
