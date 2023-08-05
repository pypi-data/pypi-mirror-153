
from contextlib import contextmanager
from wintersweet.utils.base import Utils


@contextmanager
def catch_error():
    """异常捕获，打印error级日志
    Usage：
        with catch_error():
            ...
    通过with语句捕获异常
    """

    try:

        yield

    except Exception as err:

        Utils.log.exception(err)

