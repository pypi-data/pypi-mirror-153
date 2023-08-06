import abc
from dataclasses import dataclass, field

from pathlib import Path


class ModalityFileNotFoundError(RuntimeError):
    ...


@dataclass
class Modality(abc.ABC):
    file_name: str
    read_context: dict = field(default_factory=dict)


class ModalityDescriptor(abc.ABC):
    def __init__(self, fget=None, **kwargs):
        self._fget = fget

    def __get__(self, dp, *args):
        modality = self._fget(dp)
        modality_file_path = self._get_modality_file_path(dp, modality)
        return self._read(dp, modality, modality_file_path)

    @staticmethod
    def _get_modality_file_path(dp, modality: Modality) -> Path:
        scene_modality_path = dp.scene_path.joinpath(modality.file_name)
        frame_modality_path = dp.frame_path.joinpath(modality.file_name)
        camera_modality_path = dp.camera_path.joinpath(modality.file_name)
        if scene_modality_path.exists():
            return scene_modality_path
        elif frame_modality_path.exists():
            return frame_modality_path
        elif camera_modality_path.exists():
            return camera_modality_path
        else:
            raise ModalityFileNotFoundError(f"'{modality.file_name}' not found for datapoint {dp}")

    @abc.abstractmethod
    def _read(self, dp, modality: Modality, modality_file_path: Path):
        ...


@dataclass
class TextualModality(Modality):
    factory_name: str = None


class TextualModalityDescriptor(ModalityDescriptor):
    def _read(self, dp, modality: TextualModality, modality_file_path: Path):
        return dp.modalities_container.read_textual_modality(
            modality_factory_name=modality.factory_name,
            modality_file_path=modality_file_path,
            **modality.read_context,
        )


@dataclass
class VisualModality(Modality):
    ...


class VisualModalityDescriptor(ModalityDescriptor):
    def _read(self, dp, modality: VisualModality, modality_file_path: Path):
        return dp.modalities_container.read_visual_modality(
            modality_file_path=modality_file_path, **modality.read_context
        )
