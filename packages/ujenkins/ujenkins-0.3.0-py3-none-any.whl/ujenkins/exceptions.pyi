from _typeshed import Incomplete

class JenkinsError(Exception):
    message: Incomplete
    status: Incomplete
    def __init__(self, message: Incomplete | None = ..., status: Incomplete | None = ...) -> None: ...

class JenkinsNotFoundError(JenkinsError): ...
