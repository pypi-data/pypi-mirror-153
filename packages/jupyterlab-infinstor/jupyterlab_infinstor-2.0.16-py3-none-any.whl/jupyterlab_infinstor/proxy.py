import inspect
import socket
import os
from urllib.parse import urlunparse, urlparse, quote
import aiohttp
from asyncio import Lock
import json

from tornado import gen, web, httpclient, httputil, process, websocket, ioloop, version_info

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler, utcnow

from .websocket import WebSocketHandlerMixin, pingable_ws_connect

from . import servicedefs
from .cognito_utils import perform_infinstor_login
import builtins

class ProxyHandler(WebSocketHandlerMixin, IPythonHandler):
    """
    A tornado request handler that proxies HTTP and websockets from
    a given host/port combination. This class is not meant to be
    used directly as a means of overriding CORS. This presents significant
    security risks, and could allow arbitrary remote code access. Instead, it is
    meant to be subclassed and used for proxying URLs from trusted sources.

    Subclasses should implement open, http_get, post, put, delete, head, patch,
    and options.
    """
    def __init__(self, *args, **kwargs):
        self.proxy_base = ''
        self.absolute_url = kwargs.pop('absolute_url', False)
        self.host_whitelist = kwargs.pop('host_whitelist', ['localhost', '127.0.0.1'])
        self.subprotocols = None
        super().__init__(*args, **kwargs)

    # Support all the methods that tornado does by default except for GET which
    # is passed to WebSocketHandlerMixin and then to WebSocketHandler.

    async def open(self, port, proxied_path):
        raise NotImplementedError('Subclasses of ProxyHandler should implement open')

    async def http_get(self, host, port, proxy_path=''):
        '''Our non-websocket GET.'''
        raise NotImplementedError('Subclasses of ProxyHandler should implement http_get')

    def post(self, host, port, proxy_path=''):
        raise NotImplementedError('Subclasses of ProxyHandler should implement this post')

    def put(self, port, proxy_path=''):
        raise NotImplementedError('Subclasses of ProxyHandler should implement this put')

    def delete(self, host, port, proxy_path=''):
        raise NotImplementedError('Subclasses of ProxyHandler should implement delete')

    def head(self, host, port, proxy_path=''):
        raise NotImplementedError('Subclasses of ProxyHandler should implement head')

    def patch(self, host, port, proxy_path=''):
        raise NotImplementedError('Subclasses of ProxyHandler should implement patch')

    def options(self, host, port, proxy_path=''):
        raise NotImplementedError('Subclasses of ProxyHandler should implement options')

    def on_message(self, message):
        """
        Called when we receive a message from our client.

        We proxy it to the backend.
        """
        self._record_activity()
        if hasattr(self, 'ws'):
            self.ws.write_message(message, binary=isinstance(message, bytes))

    def on_ping(self, data):
        """
        Called when the client pings our websocket connection.

        We proxy it to the backend.
        """
        self.log.debug('jupyter_server_proxy: on_ping: {}'.format(data))
        self._record_activity()
        if hasattr(self, 'ws'):
            self.ws.protocol.write_ping(data)

    def on_pong(self, data):
        """
        Called when we receive a ping back.
        """
        self.log.debug('jupyter_server_proxy: on_pong: {}'.format(data))

    def on_close(self):
        """
        Called when the client closes our websocket connection.

        We close our connection to the backend too.
        """
        if hasattr(self, 'ws'):
            self.ws.close()

    def _record_activity(self):
        """Record proxied activity as API activity

        avoids proxied traffic being ignored by the notebook's
        internal idle-shutdown mechanism
        """
        self.settings['api_last_activity'] = utcnow()

    def _get_context_path(self, port):
        """
        Some applications need to know where they are being proxied from.
        This is either:
        - {base_url}/proxy/{port}
        - {base_url}/proxy/absolute/{port}
        - {base_url}/{proxy_base}
        """
        if self.proxy_base:
            return url_path_join(self.base_url, self.proxy_base)
        if self.absolute_url:
            return url_path_join(self.base_url, 'proxy', 'absolute', str(port))
        else:
            return url_path_join(self.base_url, 'proxy', str(port))

    def get_client_uri(self, protocol, host, port, proxied_path):
        context_path = self._get_context_path(port)
        if self.absolute_url:
            client_path = url_path_join(context_path, proxied_path)
        else:
            client_path = proxied_path

        # Quote spaces, åäö and such, but only enough to send a valid web
        # request onwards. To do this, we mark the RFC 3986 specs' "reserved"
        # and "un-reserved" characters as safe that won't need quoting. The
        # un-reserved need to be marked safe to ensure the quote function behave
        # the same in py36 as py37.
        #
        # ref: https://tools.ietf.org/html/rfc3986#section-2.2
        client_path = quote(client_path, safe=":/?#[]@!$&'()*+,;=-._~")

        client_uri = '{protocol}://{host}:{port}{path}'.format(
            protocol=protocol,
            host=host,
            port=port,
            path=client_path
        )
        if self.request.query:
            client_uri += '?' + self.request.query

        return client_uri

    def _build_proxy_request(self, host, port, proxied_path, body):

        headers = self.proxy_request_headers()

        client_uri = self.get_client_uri('https', host, port, proxied_path)
        # Some applications check X-Forwarded-Context and X-ProxyContextPath
        # headers to see if and where they are being proxied from.
        if not self.absolute_url:
            context_path = self._get_context_path(port)
            headers['X-Forwarded-Context'] = context_path
            headers['X-ProxyContextPath'] = context_path

        headers['Host'] = host
        if (builtins.accesstoken.startswith('Custom')):
            headers['Authorization'] = builtins.accesstoken
        else:
            headers['Authorization'] = 'Bearer ' + builtins.accesstoken

        req = httpclient.HTTPRequest(
            client_uri, method=self.request.method, body=body,
            headers=headers, allow_nonstandard_methods=True, **self.proxy_request_options())
        return req

    def _check_host_whitelist(self, host):
        if (builtins.service == None):
            builtins.log.error('proxy: builtins.service is None. Denying access')
            return False
        elif (host == 'mlflowserver.' + builtins.service or host == 'mlflowstatic.' + builtins.service):
            return True
        else:
            builtins.log.info('proxy: Denying access to ' + str(host) + '. builtins.service is ' + builtins.service)
            return False

    @web.authenticated
    async def proxy(self, host, port, proxied_path):
        '''
        This serverextension handles:
            {base_url}/proxy/{port([0-9]+)}/{proxied_path}
            {base_url}/proxy/absolute/{port([0-9]+)}/{proxied_path}
            {base_url}/{proxy_base}/{proxied_path}
        '''

        if not self._check_host_whitelist(host):
            self.set_status(403)
            self.write("Host '{host}' is not whitelisted. "
                       "See https://jupyter-server-proxy.readthedocs.io/en/latest/arbitrary-ports-hosts.html for info.".format(host=host))
            return

        if (proxied_path == '/' or proxied_path.startswith('/static-files')):
            new_host = builtins.mlflowstaticserver
            builtins.log.info('Proxying static-files. http://' + str(host) + ':' + str(port) + str(proxied_path) + ' -> https://' + str(new_host) + str(proxied_path));
            host = new_host
            rest_call = False
        elif (proxied_path.startswith('/ajax-api/2.0/preview')):
            # builtins.log.info('Proxying REST call. before mods. host=' + str(host) + ', port=' + str(port) + ', proxied_path=' + str(proxied_path));
            new_host = builtins.mlflowserver
            new_proxied_path = '/Prod/2.0' + proxied_path[len('/ajax-api/2.0/preview'):]
            builtins.log.info('Proxying REST. http://' + str(host) + ':' + str(port) + str(proxied_path) + ' -> https://' + str(new_host) + str(new_proxied_path));
            proxied_path = new_proxied_path
            host = new_host
            rest_call = True
        elif (proxied_path.startswith('/ajax-api/2.0')):
            # builtins.log.info('Proxying REST call. before mods. host=' + str(host) + ', port=' + str(port) + ', proxied_path=' + str(proxied_path));
            new_host = builtins.mlflowserver
            new_proxied_path = '/Prod/2.0' + proxied_path[len('/ajax-api/2.0'):]
            builtins.log.info('Proxying REST. http://' + str(host) + ':' + str(port) + str(proxied_path) + ' -> https://' + str(new_host + str(new_proxied_path)));
            proxied_path = new_proxied_path
            host = new_host
            rest_call = True
        elif (proxied_path.startswith('/get-artifact')):
            new_host = builtins.mlflowserver
            new_proxied_path = '/Prod/2.0/mlflow/artifacts/get' + proxied_path[len('/get-artifact'):]
            builtins.log.info('Proxying REST. http://' + str(host) + ':' + str(port) + str(proxied_path) + ' -> https://' + str(new_host) + str(new_proxied_path));
            proxied_path = new_proxied_path
            host = new_host
            rest_call = True
        elif (proxied_path.startswith('/model-versions')):
            new_host = builtins.mlflowserver
            new_proxied_path = '/Prod/2.0/mlflow/model-versions' + proxied_path[len('/model-versions'):]
            builtins.log.info('Proxying REST. http://' + str(host) + ':' + str(port) + str(proxied_path) + ' -> https://' + str(new_host) + str(new_proxied_path));
            proxied_path = new_proxied_path
            host = new_host
            rest_call = True
        else:
            host = builtins.mlflowstaticserver


        if 'Proxy-Connection' in self.request.headers:
            del self.request.headers['Proxy-Connection']

        self._record_activity()

        if self.request.headers.get("Upgrade", "").lower() == 'websocket':
            # We wanna websocket!
            # jupyterhub/jupyter-server-proxy@36b3214
            self.log.info("we wanna websocket, but we don't define WebSocketProxyHandler")
            self.set_status(500)

        body = self.request.body
        if not body:
            if self.request.method == 'POST':
                body = b''
            else:
                body = None

        for retry in range(2):
            client = httpclient.AsyncHTTPClient()

            req = self._build_proxy_request(host, port, proxied_path, body)

            try:
                response = await client.fetch(req, raise_error=False)
            except httpclient.HTTPError as err:
                # We need to capture the timeout error even with raise_error=False,
                # because it only affects the HTTPError raised when a non-200 response
                # code is used, instead of suppressing all errors.
                # Ref: https://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.AsyncHTTPClient.fetch
                if err.code == 599:
                    self._record_activity()
                    self.set_status(599)
                    self.write(str(err))
                    return
                else:
                    raise

            # record activity at start and end of requests
            self._record_activity()

            # For all non http errors...
            if response.error and type(response.error) is not httpclient.HTTPError:
                self.set_status(500)
                self.write(str(response.error))
                return
            else:
                if (response.code == 401 and retry == 0):
                    perform_infinstor_login(builtins.cognito_username, builtins.cognito_password)
                    continue
                self.set_status(response.code, response.reason)

                # clear tornado default header
                self._headers = httputil.HTTPHeaders()

                for header, v in response.headers.get_all():
                    if header not in ('Content-Length', 'Transfer-Encoding',
                                      'Content-Encoding', 'Connection'):
                        # some header appear multiple times, eg 'Set-Cookie'
                        self.add_header(header, v)

                if response.body:
                    self.write(response.body)
                return

    async def proxy_open(self, host, port, proxied_path=''):
        """
        Called when a client opens a websocket connection.

        We establish a websocket connection to the proxied backend &
        set up a callback to relay messages through.
        """

        if not self._check_host_whitelist(host):
            self.set_status(403)
            self.log.info("Host '{host}' is not whitelisted. "
                          "See https://jupyter-server-proxy.readthedocs.io/en/latest/arbitrary-ports-hosts.html for info.".format(host=host))
            self.close()
            return

        if not proxied_path.startswith('/'):
            proxied_path = '/' + proxied_path

        client_uri = self.get_client_uri('ws', host, port, proxied_path)
        headers = self.request.headers
        current_loop = ioloop.IOLoop.current()
        ws_connected = current_loop.asyncio_loop.create_future()

        def message_cb(message):
            """
            Callback when the backend sends messages to us

            We just pass it back to the frontend
            """
            # Websockets support both string (utf-8) and binary data, so let's
            # make sure we signal that appropriately when proxying
            self._record_activity()
            if message is None:
                self.close()
            else:
                self.write_message(message, binary=isinstance(message, bytes))

        def ping_cb(data):
            """
            Callback when the backend sends pings to us.

            We just pass it back to the frontend.
            """
            self._record_activity()
            self.ping(data)

        async def start_websocket_connection():
            self.log.info('Trying to establish websocket connection to {}'.format(client_uri))
            self._record_activity()
            request = httpclient.HTTPRequest(url=client_uri, headers=headers)
            self.ws = await pingable_ws_connect(request=request,
                on_message_callback=message_cb, on_ping_callback=ping_cb,
                subprotocols=self.subprotocols)
            ws_connected.set_result(True)
            self._record_activity()
            self.log.info('Websocket connection established to {}'.format(client_uri))

        current_loop.add_callback(start_websocket_connection)
        # Wait for the WebSocket to be connected before resolving.
        # Otherwise, messages sent by the client before the
        # WebSocket successful connection would be dropped.
        await ws_connected


    def proxy_request_headers(self):
        '''A dictionary of headers to be used when constructing
        a tornado.httpclient.HTTPRequest instance for the proxy request.'''
        return self.request.headers.copy()

    def proxy_request_options(self):
        '''A dictionary of options to be used when constructing
        a tornado.httpclient.HTTPRequest instance for the proxy request.'''
        return dict(follow_redirects=False, connect_timeout=250.0, request_timeout=300.0)

    def check_xsrf_cookie(self):
        '''
        http://www.tornadoweb.org/en/stable/guide/security.html

        Defer to proxied apps.
        '''
        pass

    def select_subprotocol(self, subprotocols):
        '''Select a single Sec-WebSocket-Protocol during handshake.'''
        self.subprotocols = subprotocols
        if isinstance(subprotocols, list) and subprotocols:
            self.log.info('Client sent subprotocols: {}'.format(subprotocols))
            return subprotocols[0]
        return super().select_subprotocol(subprotocols)

class MlflowProxyHandler(ProxyHandler):
    """
    A tornado request handler that proxies HTTP and websockets
    from a port on the local system. Same as the above ProxyHandler,
    but specific to 'localhost'.
    """
    async def http_get(self, port, proxied_path):
        return await self.proxy(port, proxied_path)

    async def open(self, port, proxied_path):
        infinhost = 'mlflowserver.' + builtins.service
        return await self.proxy_open(infinhost, port, proxied_path)

    def post(self, port, proxied_path):
        return self.proxy(port, proxied_path)

    def put(self, port, proxied_path):
        return self.proxy(port, proxied_path)

    def delete(self, port, proxied_path):
        return self.proxy(port, proxied_path)

    def head(self, port, proxied_path):
        return self.proxy(port, proxied_path)

    def patch(self, port, proxied_path):
        return self.proxy(port, proxied_path)

    def options(self, port, proxied_path):
        return self.proxy(port, proxied_path)

    def proxy(self, port, proxied_path):
        infinhost = 'mlflowserver.' + builtins.service
        return super().proxy(infinhost, port, proxied_path)

