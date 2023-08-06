from typing import Awaitable, Callable, Any


class JSasync:
    """ """

    def __init__(self, waiting4: Awaitable, runnow: Callable) -> None:
        self.func = None
        self.waiting4 = waiting4
        self.runnow = runnow
        self.successor = None

    @property
    def dest(self):
        return self.successor.dest if self.successor else self.__await__()

    def then(self, f) -> Any:
        self.func = f

        async def func():
            result = await self.waiting4
            return self.func(result)

        self.successor = JSasync(func(), self.runnow)
        return self.successor

    def now(self):
        return self.runnow()

    def __await__(self):
        return self.waiting4
