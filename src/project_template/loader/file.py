"""
File loader

Write data to loader file.
"""

from project_template.constants import DEFAULT_ENCODING
from project_template.loader.base import BaseLoader

from project_template.log import get_logger

logger = get_logger(__name__)



class FileLoader(BaseLoader):
    """
    File loader
    """
    file = None

    def setup(self):
        """Open a file when init loader."""
        loader_path = self.settings.FILE_LOADER_PATH
        logger.info('Write data to %s', loader_path)
        self.file = open(loader_path, 'w', encoding=DEFAULT_ENCODING)  # pylint: disable=consider-using-with

    def load(self, data: str):
        """Write data to a file."""
        self.file.write(data)
        self.file.flush()

    def close(self):
        """Close file object when task done."""
        self.file.close()
        