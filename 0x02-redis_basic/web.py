#!/usr/bin/env python3
"""
An expiring web cache and tracker module to obtain the HTML
content of a particular URL and returns it.
"""
import redis
import requests
from typing import Callable
from functools import wraps


def count_requests(method: Callable) -> Callable:
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


def get_page(url: str) -> str:
    """
    obtain the HTML content of a particular URL and returns it.
    """
    req = requests.get(url)
    return req.text
