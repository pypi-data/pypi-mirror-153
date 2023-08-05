from djstarter import exceptions


class DJSpooferError(exceptions.AppError):
    """All Exceptions in the Spoofer App inherit from this class"""


class ProxyConnectionFailed(DJSpooferError):
    """For any failed proxy connections"""
