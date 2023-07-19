#!/usr/bin/env python3
"""
A redis model
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    count how many times methods of the Cache class
    are called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        A wrapper function that will increment the count
        for that key every time the method is called
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs for a
    particular function.
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        A wrapper function that will store the history
        of inputs and outputs for a particular function.
        """
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


def replay(method: Callable) -> Callable:
    """
    display the history of calls of a particular function.
    """
    r = redis.Redis()
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])
    count = r.get(key).decode('utf-8')

    print(f"{key} was called {count} times:")

    inputs = r.lrange(i, 0, -1)
    outputs = r.lrange(o, 0, -1)

    for k, v in zip(inputs, outputs):
        print(f"{key}(*{k.decode('utf-8')}) -> {v.decode('utf-8')}")


class Cache:
    """
    Cache class
    """

    def __init__(self):
        """
        Constructor method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        store the input data in Redis using a
        random key and return the key.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> UnionOfTypes:
        """
        convert the data back to the desired format.
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """
        convert bytes to int
        """
        try:
            return int.from_bytes(self, sys.byteorder)
        except Exception:
            return 0

    def get_str(self: bytes) -> str:
        """
        convert bytes to string
        """
        return self.decode("utf-8")
