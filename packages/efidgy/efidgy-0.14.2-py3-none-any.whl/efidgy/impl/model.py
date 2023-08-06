import efidgy

from . import fields


class Meta:
    def __init__(self, fields, primary_key=None):
        self.fields = fields
        self.primary_key = primary_key


class ModelMeta(type):
    @classmethod
    def _iter_fields(cls, obj):
        for base in obj.__bases__:
            for field_name, field in cls._iter_fields(base):
                yield field_name, field

            for field_name, field in vars(obj).items():
                if not isinstance(field, fields.Field):
                    continue
                yield field_name, field

    @classmethod
    def _repr(cls):
        def repr_impl(self):
            fields = []
            for field in self._meta.fields:
                value = getattr(self, field.name, None)
                if isinstance(value, str):
                    value = '"{}"'.format(value)
                fields.append('{}={}'.format(field.name, value))
            return '<{} {}>'.format(self.__class__.__name__, ' '.join(fields))
        return repr_impl

    def __new__(cls, name, bases, attrs):
        Model = super().__new__(cls, name, bases, attrs)

        Model.__repr__ = cls._repr()

        fields = []
        primary_key = None
        for field_name, field in cls._iter_fields(Model):
            field.name = field_name
            fields.append(field)
            if (
                field.primary_key
            ):
                assert primary_key is None, (
                    'Multiple primary keys are not allowed.'
                )
                primary_key = field

        Model._meta = Meta(fields, primary_key=primary_key)

        service = getattr(Model, 'service', None)
        if service is not None:
            service._bind(Model)

        return Model


class Model(metaclass=ModelMeta):
    _env = None

    @classmethod
    def _decode(cls, data, **kwargs):
        kw = {**kwargs}
        for field in cls._meta.fields:
            kw[field.name] = field._decode(data.get(field.name), **kwargs)
        return cls(**kw)

    def _encode(self):
        ret = {}
        for field in self._meta.fields:
            value = field._encode(getattr(self, field.name))
            if value is not None:
                ret[field.name] = value
        return ret

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if (
            self._meta.primary_key is None
            or other._meta.primary_key is None
        ):
            return self == other
        self_pk = getattr(self, self._meta.primary_key.name)
        other_pk = getattr(other, other._meta.primary_key.name)
        return self_pk == other_pk

    def _get_context(self):
        return {}

    def __init__(self, **kwargs):
        service = getattr(self, 'service', None)
        if service is not None:
            self.service = self.service()

        for field in self._meta.fields:
            setattr(self, field.name, kwargs.get(field.name))
