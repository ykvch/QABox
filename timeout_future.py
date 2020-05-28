import asyncio
import time


class TimeoutFuture(asyncio.Future):
    """
    Python asyncio Future with timeout and fallback value
    
    await on its instance returns fallback value if no set_result done within given timeout
    
    Usage:
        a = TimeoutFuture(3, 1234)
        print(await a)  # either 1234 after 3 seconds or val if a.set_result(val) is done beforehand
    """
    def __init__(self, timeout, fallback=None):
        self.timeout = timeout
        self.fallback = fallback
        super().__init__()

    async def await_impl(self):
        done, _ = await asyncio.wait([self], timeout=self.timeout)
        return next(iter(done)).result() if done else self.fallback

    def __await__(self):
        return self.await_impl().__await__()
