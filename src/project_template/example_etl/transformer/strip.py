"""Transform data and remove blank of data star and end."""

from project_template.example_etl.transformer.base import BaseTransformer

from project_template.log import get_logger

logger = get_logger(__name__)


class StripTransformer(BaseTransformer):
    """
    Transform data and remove blank of data star and end.
    """
    def transform(self, data: str) -> str:
        """Remove blank of data star and end."""
        logger.debug('Strip data: "%s"', data)
        return data.strip()
        