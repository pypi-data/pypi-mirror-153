import logging

from django.conf import settings
from djstarter import decorators

from .exceptions import IncolumitasError

logger = logging.getLogger(__name__)

BASE_URL = 'https://tls.incolumitas.com'


@decorators.wrap_exceptions(raise_as=IncolumitasError)
def tls_fingerprint(client):
    url = f'{BASE_URL}/fps'

    params = {
        'detail': '1',
    }

    r = client.get(url, params=params)
    r.raise_for_status()
    return TLSFingerprint(r.json())


class TLSFingerprint:
    def __init__(self, data):
        self.ciphers_length = data['ciphers_length']
        self.ec_point_formats = data['ec_point_formats']
        self.extensions = data['extensions']
        self.signature_algorithms_length = data['signature_algorithms_length']
        self.tls_fp = data['tls_fp']
