from abc import ABC, abstractmethod
from enum import Enum

from pathlib import Path


class ImageFormat(Enum):
    PNG = "png"
    EXR = "exr"


class ImagingLibrary(ABC):
    def read(self, image_file_path: Path, **kwargs):
        file_format = self._get_file_format(image_file_path)
        if file_format == ImageFormat.PNG.value:
            return self._read_png(image_file_path, kwargs)
        elif file_format == ImageFormat.EXR.value:
            return self._read_exr(image_file_path, kwargs)
        else:
            raise ValueError(f"Unsupported image format: {file_format}")

    @staticmethod
    def _get_file_format(image_file_path: Path) -> str:
        return image_file_path.suffix[1:]

    @abstractmethod
    def _read_png(self, image_file_path: Path, kwargs: dict):
        pass

    @abstractmethod
    def _read_exr(self, image_file_path: Path, kwargs: dict):
        pass
