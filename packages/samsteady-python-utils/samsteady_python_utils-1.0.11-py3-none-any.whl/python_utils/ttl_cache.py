import functools
from datetime import datetime

_last_result_time = None
_last_result_value = None
def ttl_cache(ttl=datetime.timedelta(hours=1)):
    def wrap(func):
        cache = {}
        @functools.wraps(func)
        def wrapped(*args, **kw):
            now = datetime.datetime.now()
            # see lru_cache for fancier alternatives
            key = tuple(args), frozenset(kw.items())
            if key not in cache or now - cache[key][0] > ttl:
                value = func(*args, **kw)
                cache[key] = (now, value)
            return cache[key][1]
        return wrapped
    return wrap