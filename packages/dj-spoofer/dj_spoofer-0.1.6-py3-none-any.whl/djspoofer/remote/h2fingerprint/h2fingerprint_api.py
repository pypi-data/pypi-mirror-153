import logging

from django.conf import settings
from djstarter import decorators

from .exceptions import H2Error

logger = logging.getLogger(__name__)


BASE_URL = 'https://www.mediasploit.com'


@decorators.wrap_exceptions(raise_as=H2Error)
def get_h2_fingerprint(client, *args, **kwargs):
    url = f'{BASE_URL}'

    headers = {
        'user-agent': client.user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'accept-encoding': 'gzip, deflate, br',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }

    r = client.get(url, headers=headers, *args, **kwargs)
    r.raise_for_status()
    return H2FingerprintResponse(r.json())


class H2FingerprintResponse:
    def __init__(self, data):
        self.fingerprint = data['fingerprint']
        self.settings_frame = data['settings_frame']
        self.window_frame = data['window_frame']
        self.header_priority_frame = data['header_priority_frame']
        self.pseudo_headers = data['pseudo_headers']
        self.user_agent = data['user_agent']
