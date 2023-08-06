import os

from . import models
from . import asyncapi
from . import exceptions
from . import tools


__all__ = [
    asyncapi,
    exceptions,
    'Env',
    models,
    tools,
    '__version__',
]


##
# Do not touch this line.
# See gitlab ci.
#
__version__ = '0.14.2'


class Env:
    def __init__(self, token=None, code=None, unit_system=None):
        self.host = os.environ.get('EFIDGY_HOST', 'console.efidgy.com')
        self.insecure = os.environ.get('EFIDGY_INSECURE', '0') != '0'
        self.token = token
        self.code = code
        self.unit_system = unit_system

    def override(self, **kwargs):
        return Env(**{
            'token': self.token,
            'code': self.code,
            'unit_system': self.unit_system,
            **kwargs,
        })


env = Env(
    token=os.environ.get('EFIDGY_ACCESS_TOKEN', None),
    code=os.environ.get('EFIDGY_CUSTOMER_CODE', None),
)
