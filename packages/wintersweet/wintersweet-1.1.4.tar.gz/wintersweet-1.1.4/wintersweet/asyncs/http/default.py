import asyncio
import json
import ssl

from pip._vendor.certifi import where
from aiohttp import http, ClientRequest, ClientResponse, ClientWebSocketResponse, ClientTimeout, TCPConnector
from aiohttp.helpers import sentinel


DEFAULT_SSL_CONTEXT = ssl.create_default_context(cafile=where())


DEFAULT_DOWNLOAD_TIMEOUT = ClientTimeout(total=5 * 600)

_DEFAULT_SESSION_ARGS = None


async def get_session_args():

    global _DEFAULT_SESSION_ARGS

    if _DEFAULT_SESSION_ARGS is None:

        _DEFAULT_SESSION_ARGS = dict(
            connector=TCPConnector(
                use_dns_cache=True,
                ttl_dns_cache=10,
                ssl=DEFAULT_SSL_CONTEXT,
                limit=100,
                limit_per_host=10,
            ),
            loop=asyncio.get_event_loop(),
            cookies=None,
            headers=None,
            skip_auto_headers=None,
            auth=None,
            json_serialize=json.dumps,
            request_class=ClientRequest,
            response_class=ClientResponse,
            ws_response_class=ClientWebSocketResponse,
            version=http.HttpVersion11,
            cookie_jar=None,
            connector_owner=False,
            raise_for_status=False,
            read_timeout=sentinel,
            conn_timeout=None,
            timeout=sentinel,
            auto_decompress=True,
            trust_env=False,
            requote_redirect_url=True,
            trace_configs=None
            )

    return _DEFAULT_SESSION_ARGS


