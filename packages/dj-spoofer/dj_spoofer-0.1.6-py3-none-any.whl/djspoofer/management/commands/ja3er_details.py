from djstarter import utils

from djspoofer import clients, commands
from djspoofer.models import Fingerprint
from djspoofer.remote.ja3er import ja3er_api


class Command(commands.ProxyCommand):
    help = 'Ja3er Check'

    def handle(self, *args, **kwargs):
        try:
            fp = Fingerprint.objects.random_desktop(browser=kwargs.get('browser'))
            with clients.desktop_client(fingerprint=fp, proxy_enabled=not kwargs['proxy_disabled']) as client:
                self.show_ja3er_details(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully got ja3er details'))

    def show_ja3er_details(self, client):
        r_json = ja3er_api.details(client)
        self.stdout.write(utils.eye_catcher_line('JA3 Details'))
        self.stdout.write(utils.pretty_dict(r_json))

        r_search = ja3er_api.search(client, ja3_hash=r_json.ja3_hash)
        self.stdout.write(utils.eye_catcher_line('JA3 Hash Search'))
        self.stdout.write(utils.pretty_dict(vars(r_search)))



