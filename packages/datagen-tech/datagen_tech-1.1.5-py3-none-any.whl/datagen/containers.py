from dependency_injector import containers, providers

from datagen.components.dataset import Dataset
from datagen.components.datasource import SourcesRepository


class DatasetContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    sources_repository = providers.Singleton(SourcesRepository)

    create = providers.Factory(Dataset, config=config, sources_repo=sources_repository)
