from urllib import request

import logging
import json

logger = logging.getLogger(__name__)


class RestClient:

    @staticmethod
    def get(url):
        response = request.urlopen(request.Request(url, method='GET'))
        return json.loads(response.decode())
