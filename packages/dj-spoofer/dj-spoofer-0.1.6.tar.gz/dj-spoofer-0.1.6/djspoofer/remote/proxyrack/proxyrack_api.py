import logging
import httpx
from django.conf import settings

from djstarter import decorators

from djspoofer.remote.proxyrack import exceptions

logger = logging.getLogger(__name__)

BASE_URL = 'http://api.proxyrack.net'


@decorators.wrap_exceptions(raise_as=exceptions.ProxyRackError)
def active_connections(client, *args, **kwargs):
    url = f'{BASE_URL}/active_conns'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return ActiveConnectionsResponse(r.json())


class ActiveConnectionsResponse:
    class Connection:
        def __init__(self, data):
            self.create_time = data['createTime']
            self.dest_addr = data['destAddr']
            self.source_addr = data['sourceAddr']

    def __init__(self, data):
        self.connections = [self.Connection(c) for c in data]


@decorators.wrap_exceptions(raise_as=exceptions.ProxyRackError)
def cities(client, *args, **kwargs):
    url = f'{BASE_URL}/cities'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return CitiesResponse(r.json())


class CitiesResponse:
    def __init__(self, data):
        self.cities = data


@decorators.wrap_exceptions(raise_as=exceptions.ProxyRackError)
def countries(client, *args, **kwargs):
    url = f'{BASE_URL}/countries'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return CountriesResponse(r.json())


class CountriesResponse:
    def __init__(self, data):
        self.countries = data


@decorators.wrap_exceptions(raise_as=exceptions.ProxyRackError)
def isps(client, country, *args, **kwargs):
    url = f'{BASE_URL}/countries/{country}/isps'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return ISPSResponse(r.json())


class ISPSResponse:
    def __init__(self, data):
        self.isps = data


@decorators.wrap_exceptions(raise_as=exceptions.ProxyRackError)
def country_ip_count(client, country, *args, **kwargs):
    url = f'{BASE_URL}/countries/{country}/count'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return r.text


@decorators.wrap_exceptions(raise_as=exceptions.ProxyRackError)
def generate_temp_api_key(client, expiration_seconds, *args, **kwargs):
    url = f'{BASE_URL}/passwords'

    params = {
        'expirationSeconds': expiration_seconds,
    }

    r = client.post(url, params=params, *args, **kwargs)
    r.raise_for_status()
    return GenerateTempApiKeyResponse(r.json())


class GenerateTempApiKeyResponse:
    class Password:
        def __init__(self, data):
            self.expiration_seconds = data['expirationSeconds']
            self.password = data['password']

    def __init__(self, data):
        self.password = self.Password(data['password'])
        self.success = data['success']

    @property
    def api_key(self):
        return self.password.password


status_errors_map = {
    407: exceptions.ProxyNotAuthenticated,
    560: exceptions.GeoLocationNotFound,
    561: exceptions.ProxyUnreachable,
    562: exceptions.ProxyNotFound,
    564: exceptions.ProxyNotOnline
}


def is_valid_proxy(proxies):
    url = 'https://api.ipify.org?format=json'
    try:
        r = httpx.get(url, proxies=proxies)
        return not r.is_error
    except httpx.TransportError as e:
        logger.warning(f'Error while testing proxies. Error: {str(e)}')
        return False


@decorators.wrap_exceptions(raise_as=exceptions.ProxyRackError)
def stats(client, *args, **kwargs):
    """
    Gets statistics of current proxy
    Note: An endpoint must be hit first, or data will be blank
    :param client:
    :param args:
    :param kwargs:
    :return:
    """

    url = f'{BASE_URL}/stats'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return StatsResponse(r.json())


class StatsResponse:
    class IPInfo:
        class Fingerprint:
            def __init__(self, data):
                self.osName = data['osName']

        def __init__(self, data):
            self.city = data['city']
            self.country = data['country']
            self.fingerprint = self.Fingerprint(data['fingerprint'])
            self.ip = data['ip']
            self.isp = data['isp']
            self.online = data['online']
            self.proxyId = data.get('proxyId')

    def __init__(self, data):
        self.ipinfo = self.IPInfo(data['ipinfo'])
        self.thread_limit = data['threadLimit']
