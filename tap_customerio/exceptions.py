class customerioError(Exception):
    """class representing Generic Http error."""

    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class customerioBackoffError(customerioError):
    """class representing backoff error handling."""
    pass

class customerioBadRequestError(customerioError):
    """class representing 400 status code."""
    pass

class customerioUnauthorizedError(customerioError):
    """class representing 401 status code."""
    pass


class customerioForbiddenError(customerioError):
    """class representing 403 status code."""
    pass

class customerioNotFoundError(customerioError):
    """class representing 404 status code."""
    pass

class customerioConflictError(customerioError):
    """class representing 409 status code."""
    pass

class customerioUnprocessableEntityError(customerioBackoffError):
    """class representing 422 status code."""
    pass

class customerioRateLimitError(customerioBackoffError):
    """class representing 429 status code."""
    pass

class customerioInternalServerError(customerioBackoffError):
    """class representing 500 status code."""
    pass

class customerioNotImplementedError(customerioBackoffError):
    """class representing 501 status code."""
    pass

class customerioBadGatewayError(customerioBackoffError):
    """class representing 502 status code."""
    pass

class customerioServiceUnavailableError(customerioBackoffError):
    """class representing 503 status code."""
    pass

ERROR_CODE_EXCEPTION_MAPPING = {
    400: {
        "raise_exception": customerioBadRequestError,
        "message": "A validation exception has occurred."
    },
    401: {
        "raise_exception": customerioUnauthorizedError,
        "message": "The access token provided is expired, revoked, malformed or invalid for other reasons."
    },
    403: {
        "raise_exception": customerioForbiddenError,
        "message": "You are missing the following required scopes: read"
    },
    404: {
        "raise_exception": customerioNotFoundError,
        "message": "The resource you have specified cannot be found."
    },
    409: {
        "raise_exception": customerioConflictError,
        "message": "The API request cannot be completed because the requested operation would conflict with an existing item."
    },
    422: {
        "raise_exception": customerioUnprocessableEntityError,
        "message": "The request content itself is not processable by the server."
    },
    429: {
        "raise_exception": customerioRateLimitError,
        "message": "The API rate limit for your organisation/application pairing has been exceeded."
    },
    500: {
        "raise_exception": customerioInternalServerError,
        "message": "The server encountered an unexpected condition which prevented" \
            " it from fulfilling the request."
    },
    501: {
        "raise_exception": customerioNotImplementedError,
        "message": "The server does not support the functionality required to fulfill the request."
    },
    502: {
        "raise_exception": customerioBadGatewayError,
        "message": "Server received an invalid response."
    },
    503: {
        "raise_exception": customerioServiceUnavailableError,
        "message": "API service is currently unavailable."
    }
}

