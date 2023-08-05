import logging
from urllib.parse import urlparse

from django.conf import settings
from djstarter import decorators

from .exceptions import CaptchaNotReady, CaptchaUnsolvable, CriticalError, WarnError, InvalidResponse, TwoCaptchaError

logger = logging.getLogger(__name__)

API_KEY = settings.TWO_CAPTCHA_API_KEY
BASE_URL = 'http://2captcha.com'

EXC_MAP = {
    'ERROR_WRONG_CAPTCHA_ID': WarnError,
    'MAX_USER_TURN': WarnError,
    'ERROR_NO_SLOT_AVAILABLE': WarnError,
    'ERROR_WRONG_USER_KEY': CriticalError,
    'ERROR_KEY_DOES_NOT_EXIST': CriticalError,
    'ERROR_ZERO_BALANCE': CriticalError,
    'IP_BANNED': CriticalError,
    'ERROR_GOOGLEKEY': CriticalError,
    'ERROR_CAPTCHA_UNSOLVABLE': CaptchaUnsolvable,
    'CAPCHA_NOT_READY':  CaptchaNotReady
}


@decorators.retry(retry_exceptions=CaptchaUnsolvable, tries=3, delay=0, backoff=0)
def get_solved_captcha(client, proxy, site_key, page_url):
    captcha_id = get_captcha_id(client=client, proxy=proxy, site_key=site_key, page_url=page_url)
    try:
        return get_solved_token(session=client, captcha_id=captcha_id)
    except Exception:
        report_bad_captcha(captcha_id)
        raise CaptchaUnsolvable(captcha_id=captcha_id)


def get_captcha_id(client, proxy, site_key, page_url, pingback=None):
    url = f'{BASE_URL}/in.php'
    proxy_type = urlparse(proxy).scheme.upper()

    params = {
        'key': API_KEY,
        'method': 'userrecaptcha',
        'googlekey': site_key,
        'pageurl': page_url,
        'json': '1',
        'proxy': proxy,
        'proxytype': proxy_type,
        'pingback': pingback
    }
    data = {
        'proxy': proxy,
        'proxytype': proxy_type
    }

    r = client.post(url, params=params, data=data, allow_redirects=False)  # Disable redirects to network splash pages
    if not r.status_code == 200:
        raise TwoCaptchaError(f'Non 200 Response. Proxy: {proxy}, Response: {r.text}')

    r_info = TwoCaptchaResponse(r.json())
    captcha_error_check(r_info)
    return r_info.request


@decorators.retry(retry_exceptions=(CaptchaNotReady,), tries=60, delay=5, backoff=1)
def get_solved_token(client, captcha_id):
    url = f'{BASE_URL}/res.php'
    params = {
        'key': API_KEY,
        'action': 'get',
        'id': captcha_id,
        'json': 1,
    }

    r = client.get(url, params=params)

    r_info = TwoCaptchaResponse(r.json())
    captcha_error_check(r_info)
    return SolvedTokenResponse(g_token=r_info.request, captcha_id=captcha_id)


@decorators.retry(retry_exceptions=(TwoCaptchaError,))
def report_bad_captcha(client, captcha_id):
    url = f'{BASE_URL}/res.php'
    params = {
        'key': API_KEY,
        'action': 'reportbad',
        'id': captcha_id,
        'json': '1',
    }

    r = client.get(url, params=params)

    r_report = TwoCaptchaResponse(r.json())
    captcha_error_check(r_report)
    if r_report.bad_captcha_reported:
        logger.info(f'Reported bad captcha id: {captcha_id}')
        return r_report
    else:
        raise TwoCaptchaError(f'Problem while reporting bad captcha: {r.text}')


@decorators.retry(retry_exceptions=(CaptchaNotReady,))
def register_pingback(client, addr):
    url = f'{BASE_URL}/res.php'
    params = {
        'key': API_KEY,
        'action': 'add_pingback',
        'addr': addr,
        'json': '1',
    }

    r = client.get(url, params=params)

    r_report = TwoCaptchaResponse(r.json())
    captcha_error_check(r_report)


def captcha_error_check(r_info):
    if r_info.status != 1:
        raise InvalidResponse(r_info)
    if exc := EXC_MAP.get(r_info.request):
        raise exc()


class TwoCaptchaResponse:
    def __init__(self, data):
        self.status = data['status']
        self.request = data['request']

    @property
    def bad_captcha_reported(self):
        return self.request == 'OK_REPORT_RECORDED'


class SolvedTokenResponse:
    def __init__(self, g_token, captcha_id):
        self.g_token = g_token
        self.captcha_id = captcha_id
