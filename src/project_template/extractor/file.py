"""
File extractor

extract data from file.
"""
from typing import Iterable

from project_template.log import get_logger
from project_template.constants import DEFAULT_ENCODING
from project_template.extractor.base import BaseExtractor

logger = get_logger(__name__)


class FileExtractor(BaseExtractor):
    """File extractor"""

    def extract(self) -> Iterable[str]:
        """Open and read file"""
        extractor_path = self.settings.FILE_EXTRACTOR_PATH
        logger.info('Extract data from %s', extractor_path)
        with open(extractor_path, 'r', encoding=DEFAULT_ENCODING) as file:
            for i in file:
                yield i
