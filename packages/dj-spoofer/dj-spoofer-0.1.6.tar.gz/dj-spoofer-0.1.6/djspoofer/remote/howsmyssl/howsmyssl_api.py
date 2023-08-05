import logging

from django.conf import settings
from djstarter import decorators

from .exceptions import HowsMySSLError

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.howsmyssl.com'


@decorators.wrap_exceptions(raise_as=HowsMySSLError)
def ssl_check(client, *args, **kwargs):
    url = f'{BASE_URL}/a/check'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return SSLCheckResponse(r.json())


class SSLCheckResponse:

    def __init__(self, data):
        self.given_cipher_suites = data['given_cipher_suites']
        self.ephemeral_keys_supported = data['ephemeral_keys_supported']
        self.session_ticket_supported = data['session_ticket_supported']
        self.tls_compression_supported = data['tls_compression_supported']
        self.unknown_cipher_suite_supported = data['unknown_cipher_suite_supported']
        self.beast_vuln = data['beast_vuln']
        self.able_to_detect_n_minus_one_splitting = data['able_to_detect_n_minus_one_splitting']
        self.insecure_cipher_suites = data['insecure_cipher_suites']
        self.tls_version = data['tls_version']
        self.rating = data['rating']
