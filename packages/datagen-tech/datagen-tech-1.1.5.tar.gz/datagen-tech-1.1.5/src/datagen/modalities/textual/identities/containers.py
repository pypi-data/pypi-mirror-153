from dependency_injector import containers, providers

from datagen.modalities.textual.base.containers import (
    BaseModalitiesContainer,
    modality_dataclass_factory,
    modality_factory,
)


class ActorMetadataModalityContainer(containers.DeclarativeContainer):

    from .actor_metadata import v1

    create = providers.FactoryAggregate({1: modality_dataclass_factory(clazz=v1.ActorMetadata)})


class FaceBoundingBoxModalityContainer(containers.DeclarativeContainer):

    from .face_bounding_box import v1

    create = providers.FactoryAggregate({1: modality_dataclass_factory(clazz=v1.FaceBoundingBox)})


class KeypointsModalityContainer(containers.DeclarativeContainer):

    from .keypoints import v1, v2

    create = providers.FactoryAggregate(
        {1: modality_dataclass_factory(clazz=v1.Keypoints), 2: modality_dataclass_factory(clazz=v2.Keypoints)}
    )


class IdentitiesModalitiesContainer(BaseModalitiesContainer):

    actor_metadata = providers.Callable(
        modality_factory, modality_container=providers.Container(ActorMetadataModalityContainer)
    )

    face_bounding_box = providers.Callable(
        modality_factory, modality_container=providers.Container(FaceBoundingBoxModalityContainer)
    )

    keypoints = providers.Callable(modality_factory, modality_container=providers.Container(KeypointsModalityContainer))
