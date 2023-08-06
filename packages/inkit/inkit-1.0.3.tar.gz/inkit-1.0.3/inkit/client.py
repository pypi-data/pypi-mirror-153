import os
import time

import requests

from requests.exceptions import RequestException

import inkit

from inkit.response_object import ResponseObject
from inkit.exceptions import InkitClientException, InkitResponseException


HOST = 'https://api.inkit.com/v1'
USER_AGENT = 'Inkit SDK'
MAX_RETRIES = 3
TIMEOUT = 15


class Client:

    def __init__(self):
        self._session = self._build_session()

    @staticmethod
    def _build_session():
        session = requests.Session()
        session.headers.update({
            'User-Agent': USER_AGENT,
            'Content-Type': 'application/json'
        })
        return session

    def send(self, path, http_method, params=None, data=None,
             retry=0, retry_interval=1, status_forcelist=None):

        if not inkit.api_token:
            raise InkitClientException(message='API Token is not specified')

        if not isinstance(inkit.api_token, str):
            raise TypeError(f'API Token must be a string, got {type(inkit.api_token)}')

        request_data = {
            'url': os.path.join(HOST, path),
            'timeout': TIMEOUT,
            'headers': {'X-Inkit-API-Token': inkit.api_token}
        }
        if data:
            request_data.update(data=data)
        if params:
            request_data.update(params=params)

        method = getattr(self._session, http_method.lower())
        return self._send_request(
            method=method,
            request_data=request_data,
            retry=retry,
            retry_interval=retry_interval,
            status_forcelist=status_forcelist or []
        )

    def _send_request(self, method, request_data, retry,
                      retry_interval, status_forcelist):

        try:
            resp = method(**request_data)

        except RequestException as e:
            raise InkitClientException(exc=e)

        if resp.ok:
            return ResponseObject(resp)

        if retry and resp.status_code in status_forcelist:
            time.sleep(retry_interval)
            return self._send_request(
                method=method,
                request_data=request_data,
                retry=retry-1,
                retry_interval=retry_interval,
                status_forcelist=status_forcelist
            )

        raise InkitResponseException(
            message='API responded with invalid status code',
            resp=ResponseObject(resp)
        )
