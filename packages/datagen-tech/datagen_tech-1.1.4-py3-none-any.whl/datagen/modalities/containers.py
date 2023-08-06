from dependency_injector import containers, providers

from datagen.imaging.opencv import OpenCVImagingLibrary
from datagen.modalities import textual as textual_modalities


class VisualModalitiesContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    imaging_library = providers.Selector(config, opencv=providers.Singleton(OpenCVImagingLibrary))


def read_visual_modality(modalities_container: containers.DeclarativeContainer, modality_file_path: str, **kwargs):
    return modalities_container.visual().imaging_library().read(image_file_path=modality_file_path, **kwargs)


def read_textual_modality(
    modalities_container: containers.DeclarativeContainer,
    modality_factory_name: str,
    modality_file_path: str,
    **modality_creation_context,
):
    return modalities_container.textual().providers[modality_factory_name](
        modality_file_path=modality_file_path, **modality_creation_context
    )


class DatapointModalitiesContainer(containers.DeclarativeContainer):

    __self__ = providers.Self()

    config = providers.Configuration()

    visual = providers.Container(VisualModalitiesContainer, config=config.imaging_library)

    read_visual_modality = providers.Callable(read_visual_modality, modalities_container=__self__)

    textual = providers.Selector(
        config.environment,
        hic=providers.Container(textual_modalities.HICModalitiesContainer),
        identities=providers.Container(textual_modalities.IdentitiesModalitiesContainer)
    )

    read_textual_modality = providers.Callable(read_textual_modality, modalities_container=__self__)

    wiring_config = containers.WiringConfiguration(packages=[textual_modalities])
