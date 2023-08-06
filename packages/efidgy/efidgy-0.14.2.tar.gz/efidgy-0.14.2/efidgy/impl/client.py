import asyncio
import json
import re
import ssl
import urllib.parse
import urllib.request

import efidgy


class Client:
    _verified = False

    def __init__(self, env):
        self.env = env
        self._context = None
        if self.env.insecure:
            self._context = ssl._create_unverified_context()

    def _url(self, path):
        args = ['time_format=clock_24']
        if self.env.unit_system is not None:
            args.append('unit_system={}'.format(self.env.unit_system))
        o = urllib.parse.urlparse(path)
        path = o.path
        if path.endswith('/'):
            path = path[:-1]
        if o.query:
            args.append(o.query)
        assert self.env.code, (
            'No customer code defined.'
        )
        return 'https://{host}/api/{code}{path}/?{args}'.format(
            host=self.env.host,
            code=self.env.code,
            path=path,
            args='&'.join(args),
        )

    def _auth(self, request):
        if self.env.token:
            request.add_header(
                'Authorization',
                'Token {}'.format(self.env.token),
            )

    def _check_api_version(self):
        if self._verified:
            return

        url = 'https://{}/efidgy_version.json'.format(self.env.host)
        try:
            with urllib.request.urlopen(url, context=self._context) as f:
                data = json.load(f)
        except (urllib.error.HTTPError, json.decoder.JSONDecodeError):
            data = None

        version = data.get('version') if data else None
        assert version, (
            'Unable to fetch server version.'
        )
        if version == 'dev':
            return
        if efidgy.__version__ == 'dev':
            return
        m = re.match(r'([^-]+)(?:-.+)?', efidgy.__version__)
        local_version = m[1] if m else efidgy.__version__
        if version != local_version:
            raise efidgy.exceptions.VersionError(version)

        type(self)._verified = True

    def _urlopen(self, url, data, method):
        self._check_api_version()

        data = json.dumps(data).encode('utf-8') if data is not None else None

        req = urllib.request.Request(url, data=data, method=method)
        self._auth(req)
        if data:
            req.add_header('Content-Type', 'application/json')

        try:
            with urllib.request.urlopen(req, context=self._context) as f:
                return json.load(f)
        except urllib.error.HTTPError as e:
            try:
                data = json.load(e)
            except json.decoder.JSONDecodeError:
                data = {}
            if e.code == 400:
                detail = data.get('detail')
                if detail is not None:
                    raise efidgy.exceptions.BadRequest(detail) from None
                raise efidgy.exceptions.ValidationError(data) from None
            if e.code == 401:
                detail = data.get(
                    'detail',
                    'Authentication failed.',
                )
                raise efidgy.exceptions.AuthenticationFailed(detail) from None
            if e.code == 403:
                detail = data.get(
                    'detail',
                    'Permission denied.',
                )
                raise efidgy.exceptions.PermissionDenied(detail) from None
            if e.code == 404:
                detail = data.get('detail', 'Not found.')
                raise efidgy.exceptions.NotFound(detail) from None
            if e.code == 405:
                detail = data.get('detail', 'Method not allowed.')
                raise efidgy.exceptions.MethodNotAllowed(detail) from None
            if e.code >= 500 and e.code < 600:
                raise efidgy.exceptions.InternalServerError() from None
            raise
        except json.decoder.JSONDecodeError:
            return None


class SyncClient(Client):
    def get(self, path):
        return self._urlopen(self._url(path), None, 'GET')

    def post(self, path, data):
        return self._urlopen(self._url(path), data, 'POST')

    def put(self, path, data):
        return self._urlopen(self._url(path), data, 'PUT')

    def delete(self, path):
        return self._urlopen(self._url(path), None, 'DELETE')


class AsyncClient(Client):
    async def _async_urlopen(self, *args):
        return await asyncio.get_event_loop().run_in_executor(
            None,
            self._urlopen,
            *args,
        )

    async def get(self, path):
        return await self._async_urlopen(self._url(path), None, 'GET')

    async def post(self, path, data):
        return await self._async_urlopen(self._url(path), data, 'POST')

    async def put(self, path, data):
        return await self._async_urlopen(self._url(path), data, 'PUT')

    async def delete(self, path):
        return await self._async_urlopen(self._url(path), None, 'DELETE')
