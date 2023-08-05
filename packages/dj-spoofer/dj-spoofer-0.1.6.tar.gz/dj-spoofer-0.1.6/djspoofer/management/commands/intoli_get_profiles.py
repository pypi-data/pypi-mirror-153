import argparse

from django.core.management.base import BaseCommand

from djspoofer.remote.intoli import tasks


class Command(BaseCommand):
    help = 'Get Intoli Profiles'

    def add_arguments(self, parser):
        parser.add_argument(
            "--max-profiles",
            required=True,
            type=int,
            help="Max Number of Intoli Profiles",
        )
        parser.add_argument(
            "--desktop-only",
            action=argparse.BooleanOptionalAction,
            help="Only Desktop Intoli Profiles",
        )
        parser.add_argument(
            "--os-list",
            required=False,
            nargs='*',
            help="Only Include Intoli Profiles that belong to OS list",
        )

    def handle(self, *args, **kwargs):
        try:
            tasks.get_profiles(**kwargs)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting profiles from Intoli'))
