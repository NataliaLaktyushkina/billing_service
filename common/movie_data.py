import json
import logging
from typing import Any

import requests

from common.core.config import settings


# create console handler and set level to debug
_log_handler = logging.StreamHandler()
_log_handler.setLevel(logging.DEBUG)


logger = logging.getLogger('movie_data')
logger.addHandler(_log_handler)
logger.setLevel(logging.DEBUG)


def check_movie_subscription(film_id: str) -> Any:
    response = requests.get(
        f'{settings.MOVIE_SERVICE}/api/v1/films/{film_id}/by_subscription',
    )
    logger.info(response.content)
    if not response.ok:
        return {}
    json_data = json.loads(response.content)
    return json_data['by_subscription']
