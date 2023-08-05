from djstarter import exceptions


class TwoCaptchaError(exceptions.ApiError):
    """Indicate generic exception that involve 2Captcha's API."""


class WarnError(TwoCaptchaError):
    """Indicate warn exception that involve 2Captcha's API."""


class CriticalError(TwoCaptchaError):
    """Indicate critical exception that involve 2Captcha's API."""


class CaptchaUnsolvable(TwoCaptchaError):
    """Indicate captcha was unsolvable."""


class CaptchaNotReady(TwoCaptchaError):
    """Captcha is not Ready Yet"""


class InvalidResponse(TwoCaptchaError):
    """Response is not valid"""
