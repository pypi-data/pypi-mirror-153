from django.conf.locale.en import formats as en_formats
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . import const, resources
from .models import Fingerprint, DeviceFingerprint, TLSFingerprint, H2Fingerprint, Proxy, IntoliFingerprint

en_formats.DATETIME_FORMAT = "M d y H:i"


@admin.register(Fingerprint)
class FingerprintAdmin(ImportExportModelAdmin):
    list_display = ['created', ]
    ordering = ['-created']
    search_fields = ['user_agent']

    show_full_result_count = False


@admin.register(DeviceFingerprint)
class DeviceFingerprintAdmin(ImportExportModelAdmin):
    list_display = ['created', 'user_agent']
    ordering = ['-created']
    search_fields = ['user_agent']

    show_full_result_count = False


@admin.register(TLSFingerprint)
class TLSFingerprintAdmin(ImportExportModelAdmin):
    list_display = ['created', 'browser', 'os', 'extensions', 'ciphers']
    list_filter = ('browser', 'os',)
    ordering = ['-created']
    search_fields = ['extensions']

    show_full_result_count = False


@admin.register(H2Fingerprint)
class H2FingerprintAdmin(ImportExportModelAdmin):
    list_display = ['created', 'browser', 'os']
    list_filter = ('browser', 'os', )
    ordering = ['-created']

    show_full_result_count = False


@admin.register(Proxy)
class ProxyAdmin(ImportExportModelAdmin):
    list_display = ['url', 'mode', 'cooldown', 'last_used', 'used_count', 'country', 'city']
    list_filter = ('mode', 'country', 'city')
    ordering = ['mode', 'url']
    search_fields = ['url']

    show_full_result_count = False
    resource_class = resources.ProxyAdminResource

    def set_rotating(self, request, queryset):
        queryset.update(mode=const.ProxyModes.ROTATING.value)

    set_rotating.short_description = 'Set as Rotating'

    def set_sticky(self, request, queryset):
        queryset.update(mode=const.ProxyModes.STICKY.value)

    set_sticky.short_description = 'Set as Sticky'

    def set_general(self, request, queryset):
        queryset.update(mode=const.ProxyModes.GENERAL.value)

    set_general.short_description = 'Set as General'

    actions = [set_rotating, set_sticky, set_general]


@admin.register(IntoliFingerprint)
class IntoliProfileAdmin(ImportExportModelAdmin):
    list_display = ['created', 'device_category', 'platform', 'user_agent', 'weight']
    list_filter = ('device_category', 'platform',)
    ordering = ['-created']
    search_fields = ['user_agent']

    show_full_result_count = False
