from dataclasses import field
from typing import TypeVar, Optional

import marshmallow
import marshmallow_dataclass
from marshmallow import pre_load, ValidationError
from marshmallow.fields import Field

from datagen.modalities.textual.common.ndarray import NumpyArray

SubSegments = TypeVar("SubSegments")


@marshmallow_dataclass.dataclass
class Keypoint:
    name: str
    coords_2d: NumpyArray = field(repr=False)
    coords_3d: NumpyArray = field(repr=False)
    is_visible: NumpyArray = field(repr=False)


class SubSegmentsField(Field):
    def _deserialize(self, value, *args, **kwargs):
        sub_segments = []
        for name, data in value.items():
            try:
                sub_segments.append(Keypoint.Schema().load({"name": name, **data}))
            except ValidationError:
                sub_segments.append(NestedSegment(name, self._deserialize(data, *args, **kwargs)))
        return sub_segments


class KeypointsSchema(marshmallow.Schema):
    TYPE_MAPPING = {SubSegments: SubSegmentsField}


@marshmallow_dataclass.dataclass(base_schema=KeypointsSchema)
class NestedSegment:
    name: str
    sub_segments: Optional[SubSegments]

    def __getattr__(self, item):
        for sub_seg in self.sub_segments:
            if sub_seg.name == item:
                return sub_seg

    def __dir__(self):
        return [seg.name for seg in self.sub_segments]


@marshmallow_dataclass.dataclass(base_schema=KeypointsSchema)
class Keypoints:
    scene: SubSegments

    def __getattr__(self, item):
        for sub_seg in self.scene:
            if sub_seg.name == item:
                return sub_seg

    def __dir__(self):
        return [seg.name for seg in self.scene]

    @pre_load
    def rearrange_fields(self, in_data: dict, **kwargs) -> dict:
        return {"scene": _convert_multi_keypoints_segments_to_matrices(in_data)}


def _convert_multi_keypoints_segments_to_matrices(in_data: dict) -> dict:
    converted_dict = {}
    for name, data in in_data.items():
        if isinstance(data, dict):
            if _is_multi_keypoints_segment(data):
                converted_dict[name] = _convert_to_matrices(data)
            else:
                converted_dict[name] = _convert_multi_keypoints_segments_to_matrices(data)
        else:
            converted_dict[name] = data
    return converted_dict


def _is_multi_keypoints_segment(in_data: dict) -> bool:
    """
    :returns True if in_data is a dictionary with numeric keys. Example:

    { "0": {...}, "1": {...}, "2": {...}, "3": {...}, ...}

    """
    return all(s.isnumeric() for s in in_data.keys())


def _convert_to_matrices(kp_num_to_kp_coords: dict) -> dict:
    """
    :returns A converted dict that represents a segments 2d an 3d keypoints matrices (Ready to parsed into numpy array)
    Example:

    {
        "coords_3d": [[1., 1., 1.], [2., 2., 2.], [3., 3., 3.], ...],
        "coords_2d":  [[1., 1.], [2., 2.], [3., 3.], ...],
        "is_visible": [True, True, True, True, ...]
    }

    """
    coords_2d_matrix, coords_3d_matrix, is_visible_arr = [], [], []
    kp_num_to_kp_coords = _convert_str_keys_to_int(kp_num_to_kp_coords)
    for _, kp_coords in sorted(kp_num_to_kp_coords.items()):
        coords_2d, coords_3d, is_visible = kp_coords["pixel_2d"], kp_coords["global_3d"], kp_coords["is_visible"]
        coords_2d_matrix.append([coords_2d["x"], coords_2d["y"]])
        coords_3d_matrix.append([coords_3d["x"], coords_3d["y"], coords_3d["z"]])
        coords_3d_matrix.append([coords_3d["x"], coords_3d["y"], coords_3d["z"]])
        is_visible_arr.append(is_visible)
    return {"coords_2d": coords_2d_matrix, "coords_3d": coords_3d_matrix, "is_visible": is_visible_arr}


def _convert_str_keys_to_int(kp_num_to_kp_coords: dict) -> dict:
    return {int(kp_num): kp_coords for kp_num, kp_coords in kp_num_to_kp_coords.items()}
