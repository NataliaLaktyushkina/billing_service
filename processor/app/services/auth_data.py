import json
from typing import Any

import requests

from core.config import settings
from core.logger import logger


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
