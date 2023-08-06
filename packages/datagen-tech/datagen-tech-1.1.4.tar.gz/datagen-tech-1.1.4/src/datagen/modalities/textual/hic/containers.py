from dependency_injector import containers, providers

from datagen.modalities.textual.base.containers import (
    BaseModalitiesContainer,
    modality_dataclass_factory,
    modality_factory,
)


class ActorsModalityContainer(containers.DeclarativeContainer):

    from .actor_metadata import v1

    create = providers.FactoryAggregate({1: modality_dataclass_factory(clazz=v1.Actors)})


class KeypointsModalityContainer(containers.DeclarativeContainer):

    from .keypoints import v1

    create = providers.FactoryAggregate({1: modality_dataclass_factory(clazz=v1.Keypoints)})


class HICModalitiesContainer(BaseModalitiesContainer):

    actors = providers.Callable(modality_factory, modality_container=providers.Container(ActorsModalityContainer))

    keypoints = providers.Callable(modality_factory, modality_container=providers.Container(KeypointsModalityContainer))
