# coding=utf-8
import inspect
from functools import partial, wraps
from typing import Callable, Iterable, TypeVar

from maxoptics.core.utils import decohints

T = TypeVar("T")
Instance = TypeVar("I")


class NONE:
    @staticmethod
    def match(dc):
        return [k for k in dc if dc[k] == NONE]


class Some:
    """Optional, provide default value if not

    .. code-block:: python
       :emphasize-lines: 3,5

       def some_function():
           interesting = False
           print 'This line is highlighted.'
           print 'This one is not...'
           print '...but this one is.'




    """

    def __init__(self, val):
        self.val = val

    @property
    def ret(self):
        return self.val

    @staticmethod
    def match(dc):
        return [k for k in dc if isinstance(dc[k], Some)]


class Currying:
    """
    The main purpose of this class is to provide highly usable currying method for FP style.

    >>> @Currying
    ... def fun(λ, e, **extra):
    ...    return λ(e, **extra)
    ...

    Of course, `fun` can be used as normal,

    >>> fun(pow, 10, exp=2)
    100

    As a curried method, it can be called as,

    >>> fun(pow)(exp=10)(2)
    1024

    Or,

    >>> fun(e=5)(exp=3)(pow)
    125

    In this way, you can easily create an easy-to-carry partial functor,

    >>> import json; fun_μ = fun(e={"μ":0}); μ_fun = fun(lambda _, **extra: str(_).encode(**extra), encoding='utf-8')
    >>> μ_fun('{"μ":0}') == fun_μ(json.dumps)
    False

    This is a specilized currying method, some traits are added to meet the functionality.

    >>> @Currying
    ... def fun(a, b=11, c=Some(22), dikt=33, **e):
    ...    print(a,b,c,dikt,e)
    ...

    `e` in `Some(e)` would be used to autofill the corresponding params if it was not set,

    >>> fun(1)
    1 11 22 33 {}

    `Some(e)` be modified if given args exceed,

    >>> fun(1,2)
    1 11 2 33 {}

    However, if the given argments still exceed, error will be raised,

    >>> fun(1,2,3)
    Traceback (most recent call last):
    ...
    TypeError: fun() tasks 2 positional arguments but 3 was given


    If mulitiple values are provided (in different calls), the later one would override the previous value,

    >>> fun(c="c1", dikt="d1")("a1"), fun(c="c1", dikt="d1")("a1", c="c2", dikt="d2")
    a1 11 c1 d1 {}
    a1 11 c2 d2 {}
    (None, None)
    """

    def __init__(self, fn):
        self.fn = fn
        self.args = []
        self.kwargs = {}
        # self.match_store = None
        self.applying = None
        self.fnargs_store = None

    def __call__(__self, *args, **kwargs):
        if not args and not kwargs:
            full_matching = __self.full_matched
            if not NONE.match(full_matching):
                ret = __self.func(**full_matching)
                try:
                    applies_iter = __self.all_applies
                    for applying in applies_iter:
                        ret.apply(applying)
                finally:
                    applies_iter.close()

                return ret
            else:
                return __self
        else:
            ret = Currying(__self)
            ret.args = args
            ret.kwargs = kwargs
            return ret()

    def apply(self: Instance, applier: Callable[[Instance], T]) -> T:
        """A method like `map` or `flatmap`.

        Args:
            applier (Callable[[Instance], T]): Method that takes `self` as input.

        Returns:
            T: The return of `applier` method.
        """
        ret = Currying(self)
        ret.applying = applier
        return ret

    def a(self: Instance, applier: Callable[[Instance], T]) -> T:
        """An alias of `apply`.

        Args:
            applier (Callable[[Instance], T]): Method that takes `self` as input.

        Returns:
            T: The return of `applier` method.
        """
        return self.apply(applier)

    def __lshift__(self, other):
        __self__ = self
        if isinstance(other, Iterable):
            for action in other:
                __self__ = __self__.apply(action)
        else:
            __self__ = __self__.apply(other)
        return __self__

    @property
    def all_applies(self):
        fn = self
        while True:
            try:
                applying = fn.applying
                if applying:
                    yield applying
                fn = fn.fn
            except AttributeError:
                break

    @property
    def func(self):
        try:
            return self.fn.func
        except AttributeError:
            return self.fn

    @property
    def fnargs(self):
        if not self.fnargs_store:
            try:
                return self.fn.fnargs
            except AttributeError:
                return inspect.getfullargspec(self.fn)

        return self.fnargs_store

    @property
    def full_matched(self):
        kwonlydefaults = self.fnargs.kwonlydefaults or {}
        ret = {**kwonlydefaults, **self.matched}
        for k in Some.match(ret):
            ret[k] = ret[k].val
        return ret

    @property
    def matched(self):
        # if not self.match_store:

        try:
            fn = self.fn
            e = fn.matched

            valid_args_len = len(NONE.match(e) + Some.match(e))
            if valid_args_len < len(self.args):
                raise TypeError(
                    f"{self.func.__name__}() tasks {valid_args_len} positional arguments but {len(self.args)} was given"
                )

            for k, v in zip(NONE.match(e) + Some.match(e), self.args):
                e[k] = v

            for k, v in self.kwargs.items():
                e[k] = v

            return e

        except AttributeError:
            args = self.fnargs.args or []
            defaults = self.fnargs.defaults or []
            defaults_dict = dict(zip(reversed(args), reversed(defaults)))
            return {**{k: NONE for k in self.fnargs.args}, **defaults_dict}

        # return self.match_store


@decohints
def currying(func: Callable[..., T]) -> Callable[..., T]:
    """This method will trick the IDE so that you can get type hint.

    Args:
        func (Callable[..., T]): the unwrapped method

    Returns:
        Callable[..., T]: the unwrapped method
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        return Currying(func)(*args, **kwargs)

    return wrapper


@decohints
def fast_currying(func: Callable[..., T]) -> Callable[..., T]:
    """Make f(x,y,z) can be called like f(x)(y)(z). And this is fast!

    Works fine with args and kwargs.

    >>> @fast_currying
    ... def f(x, y, z):
    ...     print(x, y, z)
    >>> f = f(1)
    >>> f = f(z=3)
    >>> f(2)
    1 2 3

    Will not consume TypeError (missing parameter will raise TypeError).

    >>> @fast_currying
    ... def fail(x, y):
    ...     raise TypeError("Failed if this msg is not shown")
    >>> fail(1)(2)
    Traceback (most recent call last):
        ...
    TypeError: Failed if this msg is not shown
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        pfunc = partial(func, *args, **kwargs)
        signature = inspect.signature(pfunc, follow_wrapped=False)

        try:
            signature.bind()
        except TypeError:
            return fast_currying(pfunc)
        else:
            return pfunc()

    return wrapper
