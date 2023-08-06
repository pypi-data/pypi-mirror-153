import os
from pathlib import Path

import numpy as np

from datagen.imaging.base import ImagingLibrary

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

import cv2


class OpenCVImagingLibrary(ImagingLibrary):
    def _read_png(self, image_file_path: Path, kwargs) -> np.ndarray:
        img = cv2.imread(str(image_file_path), self._get_reading_flags(kwargs))
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    def _get_reading_flags(kwargs: dict) -> int:
        return kwargs.get("opencv_reading_flags", None)

    def _read_exr(self, image_file_path: Path, kwargs) -> np.ndarray:
        img = cv2.imread(str(image_file_path), cv2.IMREAD_UNCHANGED)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
