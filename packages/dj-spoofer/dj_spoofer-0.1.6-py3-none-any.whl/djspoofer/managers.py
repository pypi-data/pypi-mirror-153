import random

from django.db import models
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone

from djspoofer import exceptions
from djspoofer.remote.intoli import exceptions as intoli_exceptions
from . import const


class GeolocationManager(models.Manager):
    pass


class H2FingerprintManager(models.Manager):
    def get_by_browser_info(self, os, browser, browser_major_version):
        q = Q(
            os=os,
            browser=browser,
            browser_min_major_version__lte=browser_major_version,
            browser_max_major_version__gte=browser_major_version
        )
        return super().get_queryset().filter(q).first()

    def get_by_oid(self, oid):
        return super().get_queryset().get(oid=oid)


class IPManager(models.Manager):
    pass


class TLSFingerprintManager(models.Manager):
    pass


class FingerprintManager(models.Manager):
    def desktop_only(self, browser=None, os=None):
        q = Q(device_fingerprint__device_category='desktop')
        if browser:
            q &= Q(device_fingerprint__browser=browser)
        if os:
            q &= Q(device_fingerprint__os=os)
        return super().get_queryset().filter(q)

    def mobile_only(self, browser=None, os=None):
        q = Q(device_fingerprint__device_category='mobile')
        if browser:
            q &= Q(device_fingerprint__browser=browser)
        if os:
            q &= Q(device_fingerprint__os=os)
        return super().get_queryset().filter(q)

    def random_desktop(self, browser=None, os=None):
        try:
            return self.desktop_only(browser=browser, os=os).order_by('?')[0]
        except Exception:
            raise exceptions.DJSpooferError(
                f'No desktop fingerprints exist for browser: {browser}, os: {os}. '
                f'Did you run the djspoofer_init command?'
            )

    def random_mobile(self, browser=None, os=None):
        try:
            return self.mobile_only(browser=browser, os=os).order_by('?')[0]
        except Exception:
            raise exceptions.DJSpooferError(
                f'No mobile fingerprints exist for browser: {browser}, os: {os}. '
                f'Did you run the djspoofer_init command?'
            )


class ProxyManager(models.Manager):

    def create_general_proxy(self, *args, **kwargs):
        return self.create(mode=const.ProxyModes.GENERAL.value, *args, **kwargs)

    def create_rotating_proxy(self, *args, **kwargs):
        return self.create(mode=const.ProxyModes.ROTATING.value, *args, **kwargs)

    def create_sticky_proxy(self, *args, **kwargs):
        return self.create(mode=const.ProxyModes.STICKY.value, *args, **kwargs)

    def get_rotating_proxy(self):
        q_filter = Q(mode=const.ProxyModes.ROTATING.value)
        try:
            return super().get_queryset().filter(q_filter)[0]
        except IndexError:
            raise exceptions.DJSpooferError('No rotating proxy is available. Did you run the djspoofer_init command?')

    def get_sticky_proxy(self):
        with transaction.atomic():
            q = Q(mode=const.ProxyModes.STICKY.value)
            q &= (Q(last_used__lt=timezone.now() - F('cooldown')) | Q(last_used=None))

            try:
                sticky_proxy = super().get_queryset().select_for_update(skip_locked=True).order_by(
                    F('last_used').asc(nulls_first=True)).filter(q)[0]
            except IndexError:
                raise exceptions.DJSpooferError('No sticky proxy is available')

            sticky_proxy.set_last_used()
            return sticky_proxy

    def get_all_urls(self):
        return super().get_queryset().values_list('url', flat=True)


class IntoliFingerprintManager(models.Manager):
    def all_oids(self):
        return super().get_queryset().values_list('oid', flat=True)

    def all_user_agents(self):
        return super().get_queryset().values_list('user_agent', flat=True)

    def all_desktop(self):
        return super().get_queryset().filter(device_category='desktop')

    def all_mobile(self):
        return super().get_queryset().filter(device_category='mobile')

    def random_desktop(self):
        try:
            return self.all_desktop().order_by('?')[0]
        except Exception:
            raise intoli_exceptions.IntoliError(
                'No Desktop Intoli Fingerprints Exist. Did you run the "intoli_get_profiles" command?'
            )

    def random_mobile(self):
        try:
            return self.all_mobile().order_by('?')[0]
        except Exception:
            raise intoli_exceptions.IntoliError(
                'No Mobile Intoli Fingerprints Exist. Did you run the "intoli_get_profiles" command?'
            )

    def weighted_n_desktop(self, count=1):
        try:
            desktop_profiles = self.all_desktop()
            weights = [float(p.weight) for p in desktop_profiles]
            return random.choices(population=desktop_profiles, weights=weights, k=count)
        except IndexError:
            raise intoli_exceptions.IntoliError('No Desktop Profiles Exist')

    def weighted_n_mobile(self, count=1):
        try:
            mobile_profiles = self.all_mobile()
            weights = [float(p.weight) for p in mobile_profiles]
            return random.choices(population=mobile_profiles, weights=weights, k=count)
        except IndexError:
            raise intoli_exceptions.IntoliError('No Mobile Profiles Exist')

    def bulk_delete(self, oids):
        return super().get_queryset().filter(oid__in=oids).delete()
