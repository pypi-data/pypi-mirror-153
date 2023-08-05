import sys
import threading
from contextlib import AbstractContextManager
from multiprocessing.context import BaseContext
from types import TracebackType
from typing import Any, Callable

__all__ = ["Lock", "RLock", "Semaphore", "BoundedSemaphore", "Condition", "Event"]

_LockLike = Lock | RLock

class Barrier(threading.Barrier):
    def __init__(
        self, parties: int, action: Callable[..., Any] | None = ..., timeout: float | None = ..., *ctx: BaseContext
    ) -> None: ...

class BoundedSemaphore(Semaphore):
    def __init__(self, value: int = ..., *, ctx: BaseContext) -> None: ...

class Condition(AbstractContextManager[bool]):
    def __init__(self, lock: _LockLike | None = ..., *, ctx: BaseContext) -> None: ...
    if sys.version_info >= (3, 7):
        def notify(self, n: int = ...) -> None: ...
    else:
        def notify(self) -> None: ...

    def notify_all(self) -> None: ...
    def wait(self, timeout: float | None = ...) -> bool: ...
    def wait_for(self, predicate: Callable[[], bool], timeout: float | None = ...) -> bool: ...
    def acquire(self, block: bool = ..., timeout: float | None = ...) -> bool: ...
    def release(self) -> None: ...
    def __exit__(
        self, __exc_type: type[BaseException] | None, __exc_val: BaseException | None, __exc_tb: TracebackType | None
    ) -> None: ...

class Event:
    def __init__(self, lock: _LockLike | None = ..., *, ctx: BaseContext) -> None: ...
    def is_set(self) -> bool: ...
    def set(self) -> None: ...
    def clear(self) -> None: ...
    def wait(self, timeout: float | None = ...) -> bool: ...

class Lock(SemLock):
    def __init__(self, *, ctx: BaseContext) -> None: ...

class RLock(SemLock):
    def __init__(self, *, ctx: BaseContext) -> None: ...

class Semaphore(SemLock):
    def __init__(self, value: int = ..., *, ctx: BaseContext) -> None: ...

# Not part of public API
class SemLock(AbstractContextManager[bool]):
    def acquire(self, block: bool = ..., timeout: float | None = ...) -> bool: ...
    def release(self) -> None: ...
    def __exit__(
        self, __exc_type: type[BaseException] | None, __exc_val: BaseException | None, __exc_tb: TracebackType | None
    ) -> None: ...
