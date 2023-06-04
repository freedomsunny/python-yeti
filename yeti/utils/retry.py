import traceback
from typing import (
    Callable,
    Awaitable,
    Any
)
import asyncio

from yeti.exceptions import exceptions

TargetFunction = Callable[..., Awaitable]


class AsyncioRetry:
    """
    asyncio retry decorator
    Usage::
        @AsyncioRetry(retry_times=3, delay=2, call_back=call_back, logger=logger)
        async def send_request():
            await req()
    """

    def __init__(self, retry_times: int = 3,
                 delay: int = 2,
                 call_back: Callable[..., Any] = None,
                 logger: Any = None):
        self.retry_times = retry_times
        self.delay = delay
        self.call_back = call_back
        self.logger = logger

    async def perform(self,
                      fn: TargetFunction,
                      retry_times: int = 3,
                      delay: int = 2,
                      call_back: Callable[..., Any] = None,
                      logger: Any = None,
                      *args,
                      **kwargs
                      ):
        """Creates a decorator function
        Args:
            fn: function
            retry_times: hwo many exec times when error happened
            delay: interval
            call_back: callback function
            logger: logging instance
        Returns:
            A wrapped function which accepts the same arguments as fn and returns an Awaitable
                ...
        """
        for i in range(retry_times):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                logger.error(traceback.format_exc())
                error_msg = "retrying times: {} execute {}".format(i + 1, fn)
                if logger:
                    logger.warning(error_msg)
                else:
                    print(error_msg)
                    print(e)
                if delay > 0:
                    await asyncio.sleep(delay)
        else:
            error_msg = f"Maximum number of <{retry_times}> retries exceeded function <{fn}>"
            if callable(call_back):
                return await call_back()
            if logger:
                logger.error(error_msg)
            else:
                print(error_msg)
            raise exceptions.InternalError

    def __call__(self, fn) -> Callable[[TargetFunction], TargetFunction]:
        async def wrapped(*args, **kwargs):
            return await self.perform(
                fn,
                retry_times=self.retry_times,
                delay=self.delay,
                call_back=self.call_back,
                logger=self.logger,
                *args,
                **kwargs
            )

        return wrapped
