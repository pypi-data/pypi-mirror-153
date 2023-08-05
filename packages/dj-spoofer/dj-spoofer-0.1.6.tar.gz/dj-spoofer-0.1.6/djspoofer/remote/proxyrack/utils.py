import random

from django.conf import settings

from . import const


class ProxyBuilder:

    def __init__(self, username, password, netloc, **options):
        self._username = username
        self._password = password
        self._netloc = netloc
        self._options = options

    @property
    def http_url(self):
        return f'http://{self._all_options}:{self._password}@{self._netloc}'

    @property
    def _all_options(self):
        return ';'.join([self._username] + [f'{k}={str(v).replace(" ", "")}' for k, v in self._options.items() if v])


def proxy_weighted_country():
    country_weights = getattr(settings, 'PROXYRACK_COUNTRY_WEIGHTS', const.DEFAULT_PROXYRACK_COUNTRY_WEIGHTS)
    countries = [c[0] for c in country_weights]
    weights = [c[1] for c in country_weights]
    return random.choices(population=countries, weights=weights, k=1)[0]


def proxy_weighted_isp():
    isp_weights = getattr(settings, 'PROXYRACK_ISP_WEIGHTS', const.DEFAULT_PROXYRACK_ISP_WEIGHTS)
    isps = [c[0] for c in isp_weights]
    weights = [c[1] for c in isp_weights]
    return random.choices(population=isps, weights=weights, k=1)[0]

