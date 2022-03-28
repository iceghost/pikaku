from collections import deque
from typing import Any, Generator, TypeVar

R = TypeVar("R")


def exhaust(gen: Generator[R, Any, Any]) -> R:
    queue = deque(gen, maxlen=1)
    return queue.pop()
