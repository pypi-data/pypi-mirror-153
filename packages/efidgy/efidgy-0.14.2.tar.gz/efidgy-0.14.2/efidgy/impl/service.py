import efidgy

from . import client


class SyncAllMixin:
    @classmethod
    def all(cls, **kwargs):
        c = client.SyncClient(cls._get_env())
        path = cls._get_path(kwargs)
        ret = []
        for data in c.get(path):
            ret.append(cls.Model._decode(data, **kwargs))
        return ret

    @classmethod
    def filter(cls, **kwargs):
        ret = []
        for o in cls.all(**kwargs):
            matched = True
            for field in o._meta.fields:
                if (
                    field.name in kwargs
                    and getattr(o, field.name) != kwargs[field.name]
                ):
                    matched = False
                    break
            if matched:
                ret.append(o)
        return ret

    @classmethod
    def first(cls, **kwargs):
        ret = cls.filter(**kwargs)
        if not ret:
            return None
        return ret[0]


class SyncGetMixin:
    @classmethod
    def get(cls, **kwargs):
        c = client.SyncClient(cls._get_env())
        path = cls._get_path(kwargs)
        pk_name = cls.Model._meta.primary_key.name
        pk = kwargs.get(pk_name, None)
        assert pk is not None, (
            'Primary key not provided: {}'.format(pk_name),
        )
        data = c.get('{}/{}'.format(path, pk))
        return cls.Model._decode(data, **kwargs)

    def refresh(self):
        pk_name = self._meta.primary_key.name
        pk = getattr(self, pk_name, None)
        kwargs = {
            **self._get_context(),
            pk_name: pk,
        }
        obj = self.get(**kwargs)
        for field in self._meta.fields:
            setattr(self, field.name, getattr(obj, field.name))


class SyncCreateMixin:
    @classmethod
    def create(cls, **kwargs):
        c = client.SyncClient(cls._get_env())
        path = cls._get_path(kwargs)
        obj = cls.Model(**kwargs)
        data = c.post(path, obj._encode())
        return cls.Model._decode(data, **kwargs)


class SyncSaveMixin:
    def save(self):
        c = client.SyncClient(self._get_env())
        path = self._get_path(self._get_context())
        c.put('{}/{}'.format(path, self.pk), self._encode(self))


class SyncDeleteMixin:
    @classmethod
    def _bind(cls, Model):
        super()._bind(Model)
        Model.delete = lambda self: self.service.delete(self)

    def delete(self, obj):
        c = client.SyncClient(self._get_env())
        path = self._get_path(obj._get_context())
        c.delete('{}/{}'.format(path, obj.pk))


class SyncViewMixin(
            SyncAllMixin,
            SyncGetMixin,
        ):
    pass


class SyncChangeMixin(
            SyncCreateMixin,
            SyncSaveMixin,
            SyncDeleteMixin,
            SyncViewMixin
        ):
    pass


class AsyncAllMixin:
    @classmethod
    async def all(cls, **kwargs):
        c = client.AsyncClient(cls._get_env())
        path = cls._get_path(kwargs)
        ret = []
        for data in await c.get(path):
            ret.append(cls.Model._decode(data, **kwargs))
        return ret

    @classmethod
    async def filter(cls, **kwargs):
        ret = []
        for o in await cls.all(**kwargs):
            matched = True
            for field, value in kwargs.items():
                if getattr(o, field, None) != value:
                    matched = False
                    break
            if matched:
                ret.append(o)
        return ret

    @classmethod
    async def first(cls, **kwargs):
        ret = await cls.filter(**kwargs)
        if not ret:
            return None
        return ret[0]


class AsyncGetMixin:
    @classmethod
    async def get(cls, **kwargs):
        c = client.AsyncClient(cls._get_env())
        path = cls._get_path(kwargs)
        pk_name = cls._meta.primary_key.name
        pk = kwargs.get(pk_name, None)
        assert pk is not None, (
            'Primary key not provided: {}'.format(pk_name),
        )
        data = await c.get('{}/{}'.format(path, pk))
        return cls._decode(data, **kwargs)

    async def refresh(self):
        pk_name = self._meta.primary_key.name
        pk = getattr(self, pk_name, None)
        kwargs = {
            **self._get_context(),
            pk_name: pk,
        }
        obj = await self.get(**kwargs)
        for field in self._meta.fields:
            setattr(self, field.name, getattr(obj, field.name))


class AsyncCreateMixin:
    @classmethod
    async def create(cls, **kwargs):
        c = client.AsyncClient(cls._get_env())
        path = cls._get_path(kwargs)
        obj = cls.Model(**kwargs)
        data = await c.post(path, obj._encode())
        return cls.Model._decode(data, **kwargs)


class AsyncSaveMixin:
    async def save(self, **kwargs):
        c = client.AsyncClient(self._get_env())
        path = self._get_path(self._get_context())
        await c.put(
            '{}/{}'.format(path, self.pk),
            self._encode(self),
        )


class AsyncDeleteMixin:
    @classmethod
    def _bind(cls, Model):
        super()._bind(Model)
        Model.delete = lambda self: self.service.delete(self)

    async def delete(self, obj):
        c = client.AsyncClient(self._get_env())
        path = self._get_path(obj._get_context())
        await c.delete('{}/{}'.format(path, obj.pk))


class AsyncViewMixin(
            AsyncAllMixin,
            AsyncGetMixin,
        ):
    pass


class AsyncChangeMixin(
            AsyncCreateMixin,
            AsyncSaveMixin,
            AsyncDeleteMixin,
            AsyncViewMixin,
        ):
    pass


class Service:
    Model = None
    path = None
    _env = None

    def __init__(self):
        assert self.path is not None, (
            'Service path must be defined: {}'.format(self)
        )

    @classmethod
    def _get_path(cls, context):
        return cls.path

    @classmethod
    def _get_env(cls):
        if cls._env is None:
            return efidgy.env
        return cls._env

    @classmethod
    def use(cls, env):
        class ProxyService(cls):
            _env = env
        return ProxyService

    @classmethod
    def _bind(cls, Model):
        cls.Model = Model


class EfidgyService(Service):
    @classmethod
    def _get_env(cls):
        return super()._get_env().override(code='efidgy')


class CustomerService(Service):
    pass


class ProjectService(CustomerService):
    @classmethod
    def _get_path(cls, context):
        project = context.get('project')
        assert project is not None, (
            'Project not passed.'
        )
        return '/projects/{project}{path}'.format(
            project=project.pk,
            path=cls.path,
        )

    def _get_context(self):
        return {
            **super()._get_context(),
            'project': self.project,
        }

    # def __init__(self, project=None, **kwargs):
    #     super().__init__(**kwargs)
    #     assert project is not None, (
    #         'Project not specified.'
    #     )
    #     self.project = project


class SolutionService(ProjectService):
    @classmethod
    def _get_path(cls, context):
        solution = context.get('solution')
        if solution is None:
            return super()._get_path(context)
        project = context['project']
        return '/projects/{project}/solutions/{solution}{path}'.format(
            project=project.pk,
            solution=solution.pk,
            path=cls.path,
        )

    def _get_context(self):
        return {
            **super()._get_context(),
            'solution': self.solution,
        }

    # def __init__(self, solution=None, **kwargs):
    #     super().__init__(**kwargs)
    #     self.solution = solution
