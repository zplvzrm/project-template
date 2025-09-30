"""Manage"""
from typing import Type

from stevedore import ExtensionManager

from project_template.config import settings
from project_template.exceptions import PluginNotFoundError
from project_template.example_etl.extractor.base import BaseExtractor
from project_template.example_etl.loader.base import BaseLoader
from project_template.example_etl.transformer.base import BaseTransformer
from project_template.log import get_logger

logger = get_logger(__name__)


class Manage:
    """Manager"""

    def __init__(self):
        self.extractor_kls: Type[BaseExtractor] = get_extension(
            'example_etl.extractor',
            settings.EXTRACTOR_NAME,
        )
        self.loader_kls: Type[BaseLoader] = get_extension(
            'example_etl.loader',
            settings.LOADER_NAME,
        )
        self.transformer_kls: Type[BaseTransformer] = get_extension(
            'example_etl.transformer',
            settings.TRANSFORMER_NAME,
        )

        self.transformer: BaseTransformer = self.transformer_kls(settings)

    def run(self):
        """Run manage"""
        with self.extractor_kls(settings) as extractor:
            with self.loader_kls(settings) as loader:
                self.transform(extractor, loader)
        logger.info('Exit example_etl.')

    def transform(self, extractor: BaseExtractor, loader: BaseLoader):
        """Transform data from extractor to loader."""
        logger.info('Start transformer data ......')
        for i in extractor.extract():
            data = self.transformer.transform(i)
            loader.load(data)

        logger.info('Data processed.')


def get_extension(namespace: str, name: str):
    """Get extension by name from namespace."""
    extension_manager = ExtensionManager(namespace=namespace, invoke_on_load=False)
    for ext in extension_manager.extensions:
        if ext.name == name:
            logger.info('Load plugin: %s in namespace "%s"', ext.plugin, namespace)
            return ext.plugin

    raise PluginNotFoundError(namespace=namespace, name=name)
    