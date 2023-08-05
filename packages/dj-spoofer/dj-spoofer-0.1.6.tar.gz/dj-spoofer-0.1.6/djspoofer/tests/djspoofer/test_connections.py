
from unittest import mock

from django.test import TestCase
from httpcore._models import Origin, Request, URL
from httpcore.backends import sync

from djspoofer import utils
from djspoofer.connections import NewHTTP2Connection


class ConnectionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.h2_fingerprint = utils.h2_hash_to_h2_fingerprint(
            os='Windows',
            browser='Firefox',
            h2_hash='1:65536;4:131072;5:16384|12517377|15:0:13:42|m,p,a,s',
            priority_frames='3:0:0:201,5:0:0:101,7:0:0:1,9:0:7:1,11:0:3:1,13:0:0:241',
            browser_min_major_version=60,
            browser_max_major_version=110,
        )

    @mock.patch.object(sync, 'SyncStream')
    def test_ok(self, mock_sync_stream):
        mock_sync_stream.write.return_value = None

        origin = Origin(
            scheme=b'http',
            host=b'www.example123xyz.com',
            port=80,
        )
        url = URL(
            url='http://www.example123xyz.com'
        )
        req = Request(
            url=url,
            method='GET',
            headers={
                b'host': 'www.example123xyz.com',
                b'h2-fingerprint-id': str(self.h2_fingerprint.oid)
            })
        new_http2_connection = NewHTTP2Connection(
            origin=origin,
            stream=mock_sync_stream(),
            keepalive_expiry=10.0
        )

        new_http2_connection._receive_response = lambda *args, **kwargs: (200, list())
        r = new_http2_connection.handle_request(req)
        self.assertEquals(r.status, 200)
