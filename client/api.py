import logging

__author__ = 'Peter Hinson'

import requests


logger = logging.getLogger('API')


class FSPAPI(object):
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        self.username = username
        self.password = password

    def run_target(self, target):
        pass

    def call(self, url, payload={}, page_size=10000):
        url = self.base_url + url
        payload['pagesize'] = page_size
        kwargs = {}

        if self.username is not None and self.password is not None:
            kwargs['auth'] = (self.username, self.password)

        response = requests.get(url, params=payload, **kwargs)

        if response.status_code != requests.codes.ok:
            logger.error('Request to %s failed with %d' % (url, response.status_code))
            response.raise_for_status()

        return response.json()

