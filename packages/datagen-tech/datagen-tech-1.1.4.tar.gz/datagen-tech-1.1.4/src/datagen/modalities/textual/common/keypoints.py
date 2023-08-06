import marshmallow_dataclass


@marshmallow_dataclass.dataclass
class Coords2D:
    x: float
    y: float


@marshmallow_dataclass.dataclass
class Coords3D:
    x: float
    y: float
    z: float
