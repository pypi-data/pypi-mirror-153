import logging

from djstarter import decorators

from .exceptions import Ja3erError

logger = logging.getLogger(__name__)

BASE_URL = 'https://ja3er.com'


@decorators.wrap_exceptions(raise_as=Ja3erError)
def details(client, *args, **kwargs):
    url = f'{BASE_URL}/json'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return DetailsResponse(r.json())


class DetailsResponse:

    def __init__(self, data):
        self.data = data
        self.ja3_hash = data['ja3_hash']
        self.ja3 = data['ja3']
        self.ja3_parts = self.ja3.split(',')
        self.user_agent = data['User-Agent']

    @property
    def ssl_version(self):
        return self.ja3_parts[0]

    @property
    def ciphers(self):
        return self.ja3_parts[1]

    @property
    def ssl_extensions(self):
        return self.ja3_parts[2]

    @property
    def elliptic_curve(self):
        return self.ja3_parts[3]

    @property
    def elliptic_curve_point_format(self):
        return self.ja3_parts[4]


@decorators.wrap_exceptions(raise_as=Ja3erError)
def search(client, ja3_hash, *args, **kwargs):
    url = f'{BASE_URL}/search/{ja3_hash}'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return SearchResponse(r.json())


class SearchResponse:

    class Stats:
        def __init__(self, data):
            self.user_agent = data['User-Agent']
            self.count = data['Count']
            self.last_seen = data['Last_seen']

    class Comment:
        def __init__(self, data):
            self.comment = data['Comment']
            self.reported = data['Reported']

    def __init__(self, data):
        self.stats = [self.Stats(s) for s in data if s.get('User-Agent')]
        self.comments = [self.Comment(c) for c in data if c.get('Comment')]
