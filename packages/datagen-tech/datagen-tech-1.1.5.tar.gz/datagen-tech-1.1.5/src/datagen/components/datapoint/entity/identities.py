import os
from dataclasses import dataclass

from deprecated.sphinx import versionchanged

from datagen import modalities
from datagen.components.datapoint.entity import base


@dataclass
class DataPoint(base.DataPoint):
    @modalities.textual_modality
    def actor_metadata(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="actor_metadata", file_name="actor_metadata.json")

    @modalities.textual_modality
    def face_bounding_box(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="face_bounding_box", file_name="face_bounding_box.json")

    @modalities.textual_modality
    @versionchanged(version='1.0', reason="New 'keypoints' modality contains both standard & dense keypoints")
    def standard_keypoints(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="keypoints", file_name="standard_keypoints.json")

    @modalities.textual_modality
    @versionchanged(version='1.0', reason="New 'keypoints' modality contains both standard & dense keypoints")
    def dense_keypoints(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="keypoints", file_name="dense_keypoints.json")

    # @modalities.textual_modality
    # def keypoints(self) -> modalities.TextualModality:
    #     return modalities.TextualModality(
    #         factory_name="keypoints", file_name=os.path.join("key_points", "all_key_points.json")
    #     )
