from datagen.components.dataset import Dataset, DatasetConfig
from datagen.containers import DatasetContainer


DEFAULT_DATASET_CONFIG = DatasetConfig(imaging_library="opencv")


def load_dataset(*dataset_sources: str, dataset_config: DatasetConfig = DEFAULT_DATASET_CONFIG) -> Dataset:
    dataset = DatasetContainer()
    return dataset.create(config=dataset_config, sources_repo__sources_paths=dataset_sources)
