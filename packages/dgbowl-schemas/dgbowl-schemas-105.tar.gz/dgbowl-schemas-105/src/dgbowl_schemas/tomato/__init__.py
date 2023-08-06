from pydantic import ValidationError
import logging
from .payload_0_1 import Payload as Payload_0_1

logger = logging.getLogger(__name__)

latest_version = "0.1"


def to_payload(**kwargs):
    models = {
        "0.1": Payload_0_1,
    }
    firste = None
    for ver, Model in models.items():
        try:
            payload = Model(**kwargs)
            return payload
        except ValidationError as e:
            logger.warning("Could not parse 'kwargs' using Payload v%s.", ver)
            logger.warning(e)
            if firste is None:
                firste = e
    raise ValueError(firste)
