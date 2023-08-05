from djstarter import utils

from djspoofer import clients, commands
from djspoofer.models import Fingerprint
from djspoofer.remote.incolumitas import incolumitas_api


class Command(commands.ProxyCommand):
    help = 'Get IP Fingerprint'

    def handle(self, *args, **kwargs):
        try:
            fp = Fingerprint.objects.random_desktop(browser=kwargs.get('browser'))
            with clients.desktop_client(fingerprint=fp, proxy_enabled=not kwargs['proxy_disabled']) as client:
                r_tls = incolumitas_api.ip_fingerprint(client, ip_addr=kwargs.get('ip_addr'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_tls))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting TLS Fingerprint'))
