# -*- coding: utf-8 -*-
import threading
import functools
import datetime

tls = threading.local()


def cached_tls_random(func):
    """
    40秒以内のアクセスならキャッシュから返す
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            storage = tls.cache
        except AttributeError:
            tls.cache = {}
            storage = tls.cache
        key_func_name = args[0].__module__ + args[0].__name__ + func.__name__

        key = '{}:{}:{}'.format(key_func_name,
                                '-'.join([str(kwargs[_]) for _ in kwargs]),
                                '-'.join([str(_) for _ in args[1:]]))

        now = datetime.datetime.now()
        if key in storage:
            value, data_created_at = storage.get(key)
            diff = now - data_created_at
            # print("total seconds:", diff.total_seconds())

            # 40秒以内のアクセスならキャッシュから返す
            if diff.total_seconds() <= 40:
                # print "[+]hit cache"
                return value
        # print("[-]not hit")
        value = func(*args, **kwargs)
        storage[key] = (value, now)
        return value

    return wrapper
