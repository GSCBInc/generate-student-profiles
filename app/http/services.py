from urllib import error
from urllib import request

import logging
import json
import time

logger = logging.getLogger(__name__)


class RestClient:

    attempt = 0
    @staticmethod
    def get(url):
        logging.info('Requesting url: %s', url)
        try:
            RestClient.attempt += 1
            response = request.urlopen(request.Request(url, method='GET')).read()
            RestClient.attempt = 0
            return json.loads(response.decode())
        except error.HTTPError:
            if RestClient.attempt < 6:
                tts = RestClient.attempt * 5
                logger.info('HTTPError occurred retrying request attempt %s in %s seconds', RestClient.attempt, tts)
                time.sleep(tts)
                return RestClient.get(url)
            else:
                logger.info('Unable to get response from the server after %s attempts', RestClient.attempt)
                pass
