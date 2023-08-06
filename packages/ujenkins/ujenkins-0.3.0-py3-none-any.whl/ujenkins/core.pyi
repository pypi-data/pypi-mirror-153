from _typeshed import Incomplete
from typing import NamedTuple
from ujenkins.endpoints import Builds as Builds, Nodes as Nodes, System as System
from ujenkins.exceptions import JenkinsError as JenkinsError, JenkinsNotFoundError as JenkinsNotFoundError

class Response(NamedTuple):
    status: Incomplete
    headers: Incomplete
    body: Incomplete

class Jenkins:
    builds: Incomplete
    nodes: Incomplete
    system: Incomplete
    def __init__(self) -> None: ...
