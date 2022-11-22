import json
import logging
from typing import Any

import requests

from common.core.config import settings


# create console handler and set level to debug
_log_handler = logging.StreamHandler()
_log_handler.setLevel(logging.DEBUG)


logger = logging.getLogger('fast_api')
logger.addHandler(_log_handler)
logger.setLevel(logging.DEBUG)


def get_data_from_auth(user_id: str) -> Any:
    params = {'user_id': user_id}
    response = requests.get(
        f'{settings.AUTH_SERVICE}/v1/user_by_id',
        params=params,
    )
    logger.info(response.content)
    if not response.ok:
        return {}
    json_data = json.loads(response.content)
    return json_data['user']
