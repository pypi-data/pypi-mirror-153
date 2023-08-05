import logging

from django.conf import settings
from djstarter import decorators

from .exceptions import IncolumitasError

logger = logging.getLogger(__name__)

BASE_URL = 'https://tcpip.incolumitas.com'


@decorators.wrap_exceptions(raise_as=IncolumitasError)
def tcpip_fingerprint(client):
    url = f'{BASE_URL}/classify'

    params = {
        'by_ip': '1',
    }

    r = client.get(url, params=params)
    r.raise_for_status()
    return TCPIPFingerprintResponse(r.json())


class TCPIPFingerprintResponse:
    class Guess:
        def __init__(self, data):
            self.os = data['os']
            self.score = data['score']

    def __init__(self, data):
        self.best_n_guesses = [self.Guess(g) for g in data['bestNGuesses']]
        self.ip = data['ip']
        self.vpn_detected = data['vpn_detected']

    @property
    def top_guess(self):
        return self.best_n_guesses[0]
