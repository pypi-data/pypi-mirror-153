class JwtValidatorException(RuntimeError):
    pass


class InvalidTokenFormatException(JwtValidatorException):
    def __init__(self) -> None:
        super().__init__('Token format is incorrect')


class InvalidApplicationIdException(JwtValidatorException):
    def __init__(self) -> None:
        super().__init__('Invalid application id')


class InvalidTokenSourceException(JwtValidatorException):
    def __init__(self) -> None:
        super().__init__('Token issuer is not trusted')


class InvalidAccessTokenException(JwtValidatorException):
    def __init__(self) -> None:
        super().__init__('Invalid access token')


class ExpiredTokenException(JwtValidatorException):
    def __init__(self) -> None:
        super().__init__('Token has expired')


class ScopeNotAllowedException(JwtValidatorException):
    def __init__(self) -> None:
        super().__init__('Token is not valid in this scope')


class InvalidPublicKeyError(JwtValidatorException):
    def __init__(self) -> None:
        super().__init__('Invalid public key')
