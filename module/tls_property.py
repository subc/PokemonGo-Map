# -*- coding: utf-8 -*-
import threading
import functools
import random

tls = threading.local()


def cached_tls_random(func):

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

        if key in storage:
            if random.randint(1, 4) != 2:
                # print "hit cache"
                return storage.get(key)
            else:
                # print "hit cache bad reload"
                pass
        value = func(*args, **kwargs)
        storage[key] = value
        return value

    return wrapper
