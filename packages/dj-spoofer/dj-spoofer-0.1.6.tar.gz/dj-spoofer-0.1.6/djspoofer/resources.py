from import_export import resources

from .models import Proxy


class ProxyAdminResource(resources.ModelResource):

    class Meta:
        model = Proxy
        import_id_fields = ('oid',)
        fields = ('oid', 'url', 'mode', 'country', 'city')
