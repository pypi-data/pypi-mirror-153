import logging

from django.conf import settings
from djstarter import decorators

from .exceptions import IncolumitasError

logger = logging.getLogger(__name__)

BASE_URL = 'https://api.incolumitas.com'


@decorators.wrap_exceptions(raise_as=IncolumitasError)
def ip_fingerprint(client, ip_addr=None):
    url = f'{BASE_URL}/datacenter'

    params = dict()

    if ip_addr:
        params['ip'] = ip_addr

    r = client.get(url, params=params)
    r.raise_for_status()
    return IPFingerprintResponse(r.json())


class IPFingerprintResponse:
    def __init__(self, data):
        self.ip = data['ip']
        self.is_datacenter = data['is_datacenter']
        self.elapsed_ms = data['elapsed_ms']
