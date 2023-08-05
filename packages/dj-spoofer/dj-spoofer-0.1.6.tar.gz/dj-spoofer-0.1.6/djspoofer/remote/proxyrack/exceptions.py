from djstarter import exceptions


class ProxyRackError(exceptions.AppError):
    """All Exceptions in the ProxyRack App inherit from this class"""


class ProxyRackApiError(exceptions.ApiError):
    """All Exceptions in the ProxyRack Api inherit from this class"""


class ProxyError(exceptions.ApiError):
    """All Proxy Exceptions"""


class ProxyNotAuthenticated(ProxyError):
    """
    Proxy Not Found - 407

    This error means that there is something wrong with your authentication credentials.

    If you are using IP whitelisting, make sure that you are connecting to your proxies from the same IP address that
    you have whitelisted in your user dashboard.

    If you are using username and password authentication, please make sure that you are using your API key as your
    password and not the password you use to log in to your Proxyrack account.


    """


class GeoLocationNotFound(ProxyError):
    """
    Geo Location Not Found - 560

    This means there are no available exit nodes for your GEO location request.

    Please double check you are using the correct country code.

    If you are using a correct country code and you are still receiving this error then you will need to try again
    later or remove the GEO targeting parameters.
    """


class ProxyUnreachable(ProxyError):
    """
    Proxy Unreachable - 561

    You will receive this error if the exit node was not reachable.

    In the odd circumstance that this happens, simply retry your connection.
    """


class ProxyNotFound(ProxyError):
    """
    Proxy Not Found - 562

    This means that we were unable to find an exit node for your request.

    If you are using any of our GEO location targeting features it may mean that there are no available nodes
    for your request.

    To avoid this simply remove your targeting features and try again.
    """


class ProxyNotOnline(ProxyError):
    """
    Proxy Not Found - 564

    This means that the proxy assigned to your session is no longer online and the request could not be completed.

    You will need to release the sticky session and retry your connection.

    Alternatively, you could wait to see if the exit node comes back online and retry again.
    """
