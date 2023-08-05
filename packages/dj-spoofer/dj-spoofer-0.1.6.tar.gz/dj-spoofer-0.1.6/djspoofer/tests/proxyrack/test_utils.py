from django.test import TestCase

from djspoofer.remote.proxyrack import const, utils


class UtilTests(TestCase):
    """
    Utility Tests
    """

    def test_proxy_builder(self):
        proxy_builder = utils.ProxyBuilder(
            username='proxyman123',
            password='goodpw567',
            netloc='megaproxy.rotating.proxyrack.net:10000',
            country='US',
            city='Seattle,New York,Los Angeles',
            isp='Verizon,Ipxo Limited',
            refreshMinutes=10,
            osName=const.ProxyOs.LINUX,
            session='13ac97fe-0f26-45ff-aeb9-2801400326ec',
            proxyIp='184.53.48.165',
            missingKey=''
        )

        self.assertEquals(
            proxy_builder.http_url,
            ('http://proxyman123;country=US;city=Seattle,NewYork,LosAngeles;isp=Verizon,IpxoLimited;refreshMinutes=10;'
             'osName=Linux;session=13ac97fe-0f26-45ff-aeb9-2801400326ec;proxyIp=184.53.48.165:'
             'goodpw567@megaproxy.rotating.proxyrack.net:10000')
        )

    def test_proxy_weighted_country(self):
        country = utils.proxy_weighted_country()
        self.assertIsNotNone(country)

    def test_proxy_weighted_isp(self):
        isp = utils.proxy_weighted_isp()
        self.assertIsNotNone(isp)
