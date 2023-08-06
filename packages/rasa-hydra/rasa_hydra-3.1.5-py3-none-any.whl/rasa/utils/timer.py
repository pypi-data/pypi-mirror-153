import asyncio
import logging
import time

logger = logging.getLogger(__name__)


def timeit(func):
    async def process(func, *args, **params):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **params)
        else:
            return func(*args, **params)

    async def helper(*args, **params):
        start = time.time()
        result = await process(func, *args, **params)
        run_time = round((time.time() - start) * 1000, 2)
        if run_time > 500:
            logger.warning(f"Function {func.__name__} finished in {run_time}ms")
        return result

    return helper
