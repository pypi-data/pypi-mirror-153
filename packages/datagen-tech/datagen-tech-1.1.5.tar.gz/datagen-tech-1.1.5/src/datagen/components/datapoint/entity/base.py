from dataclasses import dataclass, field
from pathlib import Path

import cv2
from deprecated import deprecated

from datagen import modalities
from datagen.modalities.containers import DatapointModalitiesContainer


@dataclass
class DataPoint:
    visible_spectrum_image: str
    frame_num: int
    camera: str
    scene_path: Path
    modalities_container: DatapointModalitiesContainer = field(repr=False)

    @property
    def frame_path(self) -> Path:
        return self.scene_path.joinpath("frames", str(self.frame_num).zfill(3))

    @property
    def camera_path(self) -> Path:
        if self.frame_path.exists():
            return self.frame_path.joinpath(self.camera)
        else:
            return self.scene_path.joinpath(self.camera)

    @modalities.visual_modality
    def visible_spectrum(self) -> modalities.VisualModality:
        return modalities.VisualModality(self.visible_spectrum_image)

    @modalities.textual_modality
    def camera_metadata(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="camera_metadata", file_name="camera_metadata.json")

    @modalities.visual_modality
    def semantic_segmentation(self) -> modalities.VisualModality:
        if self._semantic_seg_as_png:
            return modalities.VisualModality(
                "semantic_segmentation.png", read_context={"opencv_reading_flags": cv2.IMREAD_UNCHANGED}
            )
        else:
            return modalities.VisualModality("semantic_segmentation.exr")

    @property
    def _semantic_seg_as_png(self) -> bool:
        return self.camera_path.joinpath("semantic_segmentation.png").exists()

    @modalities.textual_modality
    def semantic_segmentation_color_map(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="segmentation", file_name="semantic_segmentation_metadata.json")

    @property
    @deprecated(reason="Modality name changed to 'semantic_segmentation_color_map', please use new name instead")
    def semantic_segmentation_metadata(self):
        return self.semantic_segmentation_color_map

    @modalities.visual_modality
    def depth(self) -> modalities.VisualModality:
        return modalities.VisualModality("depth.exr")

    @modalities.visual_modality
    def normals_map(self) -> modalities.VisualModality:
        return modalities.VisualModality("normal_maps.exr")

    @property
    @deprecated(reason="Modality name changed to 'normals_map', please use new name instead")
    def normal_maps(self):
        return self.normals_map

    @modalities.visual_modality
    def infra_red(self) -> modalities.VisualModality:
        return modalities.VisualModality("infra_red.png")

    @modalities.textual_modality
    def _environments(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="environments", file_name="environment.json")

    @property
    def environment(self):
        return self._environments[self.visible_spectrum_image]
