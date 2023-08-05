import json
import ssl

from pip._vendor.certifi import where
from aiohttp import http, ClientRequest, ClientResponse, ClientWebSocketResponse, ClientTimeout, TCPConnector
from aiohttp.helpers import sentinel


DEFAULT_SSL_CONTEXT = ssl.create_default_context(cafile=where())


DEFAULT_DOWNLOAD_TIMEOUT = ClientTimeout(total=5 * 600)


DEFAULT_SESSION_ARGS = dict(
                            connector=TCPConnector(
                                use_dns_cache=True,
                                ttl_dns_cache=10,
                                ssl=DEFAULT_SSL_CONTEXT,
                                limit=100,
                                limit_per_host=10,
                            ),
                            loop=None,
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



