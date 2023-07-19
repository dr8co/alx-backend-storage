#!/usr/bin/env python3
"""
An expiring web cache and tracker
"""

import redis
import requests
from typing import Callable
from functools import wraps

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Count the number of requests
    """
    @wraps(method)
    def wrapper(url):
        """
        A wrapper function that will count the number of requests
        """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    get_page function
    """
    req = requests.get(url)
    return req.text
