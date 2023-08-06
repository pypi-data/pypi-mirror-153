import json
from functools import lru_cache, partial

from dependency_injector import containers, providers
from packaging import version

INITIAL_MODALITIES_VERSION = "1.0.0"


@lru_cache(maxsize=None)
def modality_factory(modality_container: providers.Container, modality_file_path: str, **modality_creation_context):
    """
    Important - Please note this function caches its return values!
    """
    modality_params, modality_version = _parse_modality_file(modality_file_path)
    return modality_container.create(modality_version, modality_params=modality_params, **modality_creation_context)


def _parse_modality_file(modality_file_path: str) -> tuple:
    with open(modality_file_path) as f:
        modality_params = json.load(f)
        modality_version = _get_modality_version(modality_params)
    return modality_params, modality_version


def _get_modality_version(modality_params: dict) -> int:
    modality_version = modality_params.pop("version", INITIAL_MODALITIES_VERSION)
    modality_version_ = version.parse(modality_version).major
    return modality_version_


def load_dataclass(clazz: type, modality_params: dict, **modality_creation_context):
    class_schema = clazz.Schema()
    class_schema.context.update(**modality_creation_context)
    return class_schema.load(modality_params)


modality_dataclass_factory = partial(providers.Factory, load_dataclass)


class CameraMetadataModalityContainer(containers.DeclarativeContainer):

    from .camera_metadata import v1

    create = providers.FactoryAggregate({1: modality_dataclass_factory(clazz=v1.CameraMetadata)})


class EnvironmentsModalityContainer(containers.DeclarativeContainer):

    from .environments import v1

    create = providers.FactoryAggregate({1: modality_dataclass_factory(clazz=v1.Environments)})


class SegmentationModalityContainer(containers.DeclarativeContainer):

    from .segmentation import v1

    create = providers.FactoryAggregate({1: modality_dataclass_factory(clazz=v1.Segmentation)})


class BaseModalitiesContainer(containers.DeclarativeContainer):

    camera_metadata = providers.Callable(
        modality_factory, modality_container=providers.Container(CameraMetadataModalityContainer)
    )

    environments = providers.Callable(
        modality_factory, modality_container=providers.Container(EnvironmentsModalityContainer)
    )

    segmentation = providers.Callable(
        modality_factory, modality_container=providers.Container(SegmentationModalityContainer)
    )
