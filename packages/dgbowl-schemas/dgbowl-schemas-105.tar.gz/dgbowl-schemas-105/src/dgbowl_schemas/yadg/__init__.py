from pydantic import ValidationError
import logging
from .dataschema_4_1 import DataSchema as DataSchema_4_1
from .dataschema_4_0 import DataSchema as DataSchema_4_0

logger = logging.getLogger(__name__)

latest_version = "4.1.1"
DataSchema = DataSchema_4_1


def to_dataschema(**kwargs):
    models = {
        "4.1.1": DataSchema_4_1,
        "4.0.1": DataSchema_4_0,
    }
    firste = None
    for ver, Model in models.items():
        try:
            schema = Model(**kwargs)
            return schema
        except ValidationError as e:
            logger.warning("Could not parse 'kwargs' using DataSchema v%s.", ver)
            logger.warning(e)
            if firste is None:
                firste = e
    raise ValueError(firste)
