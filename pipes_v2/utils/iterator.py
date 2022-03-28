from collections import deque
from typing import Any, Iterator, TypeVar

Item = TypeVar("Item")


def exhaust(iterator: Iterator[Item]) -> Item:
    queue = deque(iterator, maxlen=1)
    return queue.pop()

def count(iterator: Iterator[Any]):
    return sum([1 for _ in iterator])