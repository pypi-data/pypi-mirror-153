from dependency_injector import containers, providers

from datagen.components.datapoint import DatapointsRepository
from datagen.components.datapoint import HICDataPoint, IdentitiesDataPoint
from datagen.modalities.containers import DatapointModalitiesContainer


class DatapointsContainer(containers.DeclarativeContainer):

    __self__ = providers.Self()

    config = providers.Configuration()

    modalities = providers.Container(DatapointModalitiesContainer, config=config)

    factory = providers.Selector(
        config.environment,
        hic=providers.Factory(HICDataPoint, modalities_container=modalities),
        identities=providers.Factory(IdentitiesDataPoint, modalities_container=modalities)
    )

    repo = providers.Factory(DatapointsRepository, __self__)
