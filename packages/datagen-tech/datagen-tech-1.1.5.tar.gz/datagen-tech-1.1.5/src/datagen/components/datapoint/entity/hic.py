import os

from deprecated import deprecated

from datagen import modalities
from datagen.components.datapoint.entity import base


class DataPoint(base.DataPoint):
    @modalities.textual_modality
    def actors(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="actors", file_name="actor_metadata.json")

    @property
    @deprecated(reason="(Modality name changed to 'actors' (For HIC datapoints only!), please use new name instead")
    def actor_metadata(self) -> modalities.TextualModality:
        return self.actors

    @modalities.textual_modality
    def keypoints(self) -> modalities.TextualModality:
        return modalities.TextualModality(
            factory_name="keypoints", file_name=os.path.join("key_points", "all_key_points.json")
        )
