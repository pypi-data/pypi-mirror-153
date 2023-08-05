from django.conf import settings
from djstarter import utils

from djspoofer import clients, commands
from djspoofer.models import Fingerprint
from djspoofer.remote.h2fingerprint import h2fingerprint_api
from djspoofer.remote.howsmyssl import howsmyssl_api
from djspoofer.remote.incolumitas import incolumitas_api, incolumitas_tcpip_api, incolumitas_tls_api
from djspoofer.remote.ja3er import ja3er_api
from djspoofer.remote.proxyrack import utils as pr_utils


class Command(commands.ProxyCommand):
    help = 'Get All Chrome Fingerprints'

    def handle(self, *args, **kwargs):
        try:
            fp = Fingerprint.objects.random_desktop(browser=kwargs.get('browser'))
            with clients.desktop_client(fingerprint=fp, proxy_enabled=not kwargs['proxy_disabled']) as client:
                self.show_ja3er_details(client)
                self.show_ssl_check(client)
                self.show_ip_fingerprint(client)
                self.show_tcpip_fingerprint(client)
                self.show_tls_fingerprint(client)
                self.show_h2_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting All Fingerprints'))

    def proxy_http_url(self, proxy_url, proxy_args):
        proxy_builder = pr_utils.ProxyBuilder(
            netloc=proxy_url,
            password=settings.PROXY_PASSWORD,
            username=settings.PROXY_USERNAME,
            **self.proxy_options(proxy_args),
        )
        return proxy_builder.http_url

    def show_ip_fingerprint(self, client):
        r_tls = incolumitas_api.ip_fingerprint(client)
        self.stdout.write(utils.eye_catcher_line('IP Fingerprint'))
        self.stdout.write(utils.pretty_dict(r_tls))

    def show_tcpip_fingerprint(self, client):
        r_tcpip = incolumitas_tcpip_api.tcpip_fingerprint(client)
        self.stdout.write(utils.eye_catcher_line('TCP/IP Fingerprint'))
        self.stdout.write(utils.pretty_dict(r_tcpip))

    def show_tls_fingerprint(self, client):
        try:
            r_tls = incolumitas_tls_api.tls_fingerprint(client)
            self.stdout.write(utils.eye_catcher_line('TLS Fingerprint'))
            self.stdout.write(utils.pretty_dict(r_tls))
        except Exception as e:
            self.stdout.write(utils.eye_catcher_line(f'TLS Fingerprint Failed: {str(e)}'))

    def show_ja3er_details(self, client):
        r_json = ja3er_api.details(client)
        self.stdout.write(utils.eye_catcher_line('JA3 Details'))
        self.stdout.write(utils.pretty_dict(r_json))

        r_search = ja3er_api.search(client, ja3_hash=r_json.ja3_hash)
        self.stdout.write(utils.eye_catcher_line('JA3 Hash Search'))
        self.stdout.write(utils.pretty_dict(vars(r_search)))

    def show_ssl_check(self, client):
        self.stdout.write(utils.eye_catcher_line('SSL Check'))
        try:
            r_check = howsmyssl_api.ssl_check(client)
            self.stdout.write(utils.pretty_dict(vars(r_check)))
        except Exception as e:
            self.stdout.write(utils.eye_catcher_line(f'SSL Check Failed: {str(e)}'))

    def show_h2_fingerprint(self, client):
        self.stdout.write(utils.eye_catcher_line('H2 Fingerprint Check'))
        try:
            r_h2 = h2fingerprint_api.get_h2_fingerprint(client)
            self.stdout.write(utils.pretty_dict(vars(r_h2)))
        except Exception as e:
            self.stdout.write(utils.eye_catcher_line(f'H2 Fingerprint Check Failed: {str(e)}'))

    @staticmethod
    def proxy_options(proxy_args):
        return {args.split('=')[0]: args.split('=')[1] for args in proxy_args}
