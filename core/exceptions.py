class ServiceError(Exception):
    def __init__(self, message, service):
        super().__init__(message)
        self.service = service


class TransientError(ServiceError):
    pass


class PermanentError(ServiceError):
    pass


class AuthenticationError(PermanentError):
    pass


class QuotaExceededError(PermanentError):
    pass
