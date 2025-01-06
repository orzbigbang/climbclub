from fastapi import status, HTTPException


class BadRequestError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "bad request" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class AuthorizationError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "user unauthorized" if detail is None else detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class TokenInvalidError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not validate credentials" if detail is None else detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class DigestAuthError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "digest auth error" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class TokenRefreshError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_402_PAYMENT_REQUIRED
        self.detail = "token need to be refreshed" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class ForbiddenError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "authority level is lower than the resource level" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class NotFoundError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "not found" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class AlreadyExistError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "already exists" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class PreconditionFailedError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_412_PRECONDITION_FAILED
        self.detail = "user name incorrect" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class TooLargeEntityError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        self.detail = "request body too large" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class UnprocessableEntityError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        self.detail = "invalid-json" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)


class InternalServerError(HTTPException):
    def __init__(self, detail=None, headers=None):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "server error happened" if detail is None else detail
        self.headers = headers
        HTTPException(status_code=self.status_code, detail=self.detail, headers=self.headers)
