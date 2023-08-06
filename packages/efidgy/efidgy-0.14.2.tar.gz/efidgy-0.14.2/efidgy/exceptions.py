class EfidgyException(Exception):
    pass


class VersionError(EfidgyException):
    def __init__(self, server_version):
        super().__init__(
            'Update client to version: {}'.format(server_version),
        )


class BadRequest(EfidgyException):
    pass


class ValidationError(BadRequest):
    pass


class AuthenticationFailed(EfidgyException):
    pass


class PermissionDeined(EfidgyException):
    pass


class NotFound(EfidgyException):
    pass


class MethodNotAllowed(EfidgyException):
    pass


class InternalServerError(EfidgyException):
    pass


class GeocodeError(EfidgyException):
    def __init__(self, address):
        super().__init__(address)
        self.address = address
