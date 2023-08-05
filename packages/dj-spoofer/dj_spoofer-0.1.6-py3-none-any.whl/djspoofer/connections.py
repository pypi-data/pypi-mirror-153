import collections
import logging
import time
import random

import h2
from h2 import connection
from h2.exceptions import NoAvailableStreamIDError
from h2.settings import Settings, SettingCodes
from hpack import Decoder, Encoder
from hpack.table import HeaderTable
from httpcore._models import Request, Response
from httpcore._sync import http2

from djspoofer import exceptions, utils as sp_utils
from djspoofer.models import H2Fingerprint

logger = logging.getLogger(__name__)


class NewHTTP2Connection(http2.HTTP2Connection):
    H2_FINGERPRINT_HEADER = b'h2-fingerprint-id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._h2_fingerprint = None

    def _init_h2_fingerprint(self, request: Request):
        for i, (h_key, h_val) in enumerate(request.headers):
            if h_key == self.H2_FINGERPRINT_HEADER:
                self._h2_fingerprint = H2Fingerprint.objects.get_by_oid(str(h_val, 'utf-8'))
                logger.debug(f'Using H2 Fingerprint: {self._h2_fingerprint}')
                return
        raise exceptions.DJSpooferError(f'Header "{self.H2_FINGERPRINT_HEADER}" missing')

    def handle_request(self, request: Request) -> Response:
        self._init_h2_fingerprint(request)
        self._h2_state = NewH2Connection(config=self.CONFIG, h2_fingerprint=self._h2_fingerprint)
        return super().handle_request(request)

    def _send_connection_init(self, request: Request) -> None:
        """
            The HTTP/2 connection requires some initial setup before we can start
            using individual request/response streams on it.
        """

        self._h2_state.initiate_connection()
        self._h2_state.increment_flow_control_window(self._h2_fingerprint.window_update_increment)
        self._add_priority_frames()

        self._write_outgoing_data(request)

    def _send_request_headers(self, request: Request, stream_id: int) -> None:
        end_stream = not http2.has_body_headers(request)

        headers = self._get_psuedo_headers(request, h2_fingerprint=self._h2_fingerprint) + [
            (k.lower(), v)
            for k, v in request.headers
            if k.lower() not in (
                b"host",
                b"transfer-encoding",
                self.H2_FINGERPRINT_HEADER
            )
        ]

        self._h2_state.send_headers(
            stream_id,
            headers,
            end_stream=end_stream,
            priority_exclusive=bool(self._h2_fingerprint.header_priority_exclusive_bit),
            priority_depends_on=self._h2_fingerprint.header_priority_depends_on_id,
            priority_weight=self._h2_fingerprint.header_priority_weight,
        )
        if self._h2_fingerprint.browser in ('Firefox',):
            self._h2_state.increment_flow_control_window(
                self._h2_fingerprint.window_update_increment, stream_id=stream_id
            )
        self._write_outgoing_data(request)

    def _write_outgoing_data(self, request: Request) -> None:
        time.sleep(random.uniform(.06, .1))     # Small delay ensures packets are chunked into separate packets
        # TODO Investigate better way to separate packets
        super()._write_outgoing_data(request)

    def _add_priority_frames(self):
        if priority_frames := self._h2_fingerprint.priority_frames:
            for pf in sp_utils.PriorityFrameParser(priority_frames).frames:
                self._h2_state.prioritize(
                    stream_id=pf.stream_id,
                    exclusive=bool(pf.exclusivity_bit),
                    depends_on=pf.dependent_stream_id,
                    weight=pf.weight
                )

    @staticmethod
    def _get_psuedo_headers(request, h2_fingerprint):
        # In HTTP/2 the ':authority' pseudo-header is used instead of 'Host'.
        # In order to gracefully handle HTTP/1.1 and HTTP/2 we always require
        # HTTP/1.1 style headers, and map them appropriately if we end up on
        # an HTTP/2 connection.
        authority = [v for k, v in request.headers if k.lower() == b"host"][0]

        header_map = {
            'm': (b":method", request.method),
            'a': (b":authority", authority),
            's': (b":scheme", request.url.scheme),
            'p': (b":path", request.url.target),
        }
        return [header_map[k] for k in h2_fingerprint.psuedo_header_order.split(',')]


class NewH2Connection(connection.H2Connection):
    def __init__(self, h2_fingerprint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._h2_fingerprint = h2_fingerprint
        self.encoder = NewEncoder(self._h2_fingerprint)
        self.decoder = NewDecoder(self._h2_fingerprint)
        self.local_settings = NewSettings(self._h2_fingerprint)

    def get_next_available_stream_id(self):
        """
        Returns an integer suitable for use as the stream ID for the next
        stream created by this endpoint. For server endpoints, this stream ID
        will be even. For client endpoints, this stream ID will be odd. If no
        stream IDs are available, raises :class:`NoAvailableStreamIDError
        <h2.exceptions.NoAvailableStreamIDError>`.

        .. warning:: The return value from this function does not change until
                     the stream ID has actually been used by sending or pushing
                     headers on that stream. For that reason, it should be
                     called as close as possible to the actual use of the
                     stream ID.

        .. versionadded:: 2.0.0

        :raises: :class:`NoAvailableStreamIDError
            <h2.exceptions.NoAvailableStreamIDError>`
        :returns: The next free stream ID this peer can use to initiate a
            stream.
        :rtype: ``int``
        """
        # No streams have been opened yet, so return the lowest allowed stream
        # ID.
        if not self.highest_outbound_stream_id:
            next_stream_id = self._h2_fingerprint.header_priority_stream_id if self.config.client_side else 2
        else:
            next_stream_id = self.highest_outbound_stream_id + 2
        self.config.logger.debug(
            "Next available stream ID %d", next_stream_id
        )
        if next_stream_id > self.HIGHEST_ALLOWED_STREAM_ID:
            raise NoAvailableStreamIDError("Exhausted allowed stream IDs")

        return next_stream_id


class NewSettings(h2.settings.Settings):
    """
        Allows for setting the settings value in any particular order.
        There is no validation of settings since validation throws errors for missing or invalid values
        Use with caution!
    """
    def __init__(self, h2_fingerprint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h2_fingerprint = h2_fingerprint
        self._settings = self.get_initial_values()

    def get_initial_values(self):
        h2_fp = self.h2_fingerprint
        initial_values = {
            SettingCodes.HEADER_TABLE_SIZE: h2_fp.header_table_size,                            # 0x01 (Required)
            SettingCodes.ENABLE_PUSH: int(h2_fp.enable_push) if h2_fp.enable_push else None,    # 0x02 (Required)
            SettingCodes.MAX_CONCURRENT_STREAMS: h2_fp.max_concurrent_streams,                  # 0x03 (Optional)
            SettingCodes.INITIAL_WINDOW_SIZE: h2_fp.initial_window_size,                        # 0x04 (Required)
            SettingCodes.MAX_FRAME_SIZE: h2_fp.max_frame_size,                                  # 0x05 (Required)
            SettingCodes.MAX_HEADER_LIST_SIZE: h2_fp.max_header_list_size,                      # 0x06 (Optional)
        }
        return {k: collections.deque([v]) for k, v in initial_values.items() if v is not None}


class NewDecoder(Decoder):
    def __init__(self, h2_fingerprint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_table = NewHeaderTable(h2_fingerprint)
        # self.max_header_list_size = h2_fingerprint.max_header_list_size   # Firefox has no max header list size
        self.max_allowed_table_size = self.header_table.maxsize


class NewEncoder(Encoder):
    def __init__(self, h2_fingerprint):
        super().__init__()
        self.header_table = NewHeaderTable(h2_fingerprint)


class NewHeaderTable(HeaderTable):
    def __init__(self, h2_fingerprint):
        super().__init__()
        self._maxsize = h2_fingerprint.header_table_size
