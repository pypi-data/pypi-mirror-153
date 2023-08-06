import functools

import grpc


class AgentException(IOError):
    """An exception has occured while communicating with the Formant agent."""


class Unavailable(AgentException):
    """
    The Formant agent is unavailable.
    It may be updating, not running, or running with a different address.
    """


class Throttled(AgentException):
    """
    The Formant agent has throttled a datapoint, and did not ingest it.
    This happens when datapoints are posted to a unique stream + tags pair,
    with frequency greater than the stream's frequency configuration.
    Note that events can still be triggered by datapoints that are throttled.
    """


class InvalidArgument(AgentException):
    """One or more arguments were invalid."""


class Unknown(AgentException):
    """An unknown error occurred."""


RPC_ERROR_CODE_MAPPING = {
    grpc.StatusCode.UNAVAILABLE: Unavailable,
    grpc.StatusCode.RESOURCE_EXHAUSTED: Throttled,
    grpc.StatusCode.INVALID_ARGUMENT: InvalidArgument,
    grpc.StatusCode.UNKNOWN: Unknown,
}


def handle_agent_exceptions(func):
    @functools.wraps(func)
    def _handle_agent_exceptions_inner(*args, **kwargs):
        error = None
        try:
            return func(*args, **kwargs)
        except grpc.RpcError as e:
            error = e

        code = error.code() if hasattr(error, "code") else None
        if (
            (code is None)
            or (args[0].ignore_throttled and code == grpc.StatusCode.RESOURCE_EXHAUSTED)
            or (args[0].ignore_unavailable and code == grpc.StatusCode.UNAVAILABLE)
        ):
            return

        raise_exception(error, code)

    return _handle_agent_exceptions_inner


def raise_exception(error, code):
    exception_cls = RPC_ERROR_CODE_MAPPING.get(code, AgentException)
    message = str(error.details()) + "\n" + exception_cls.__doc__
    raise exception_cls(message)
