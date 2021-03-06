from hashlib import sha1
import math
from random import randint

from django.core.cache import cache
from django.db.models import Model


def cache_result(seconds=3600, expiry_variance=0.2, override_key=None):
    def doCache(f):
        def x(*args, **kwargs):

            # Don't bother if seconds is set to 0
            if not seconds:
                return f(*args, **kwargs)

            # Generate the key from the function name and given arguments.
            key = sha1(override_key or u"//".join(
                (
                    str(f),
                    u"//".join(
                        object_to_string(a) for a in args
                    ),
                    u"//".join(
                        str(a.updated) for a in args if hasattr(a, "updated")
                    ),
                    u"//".join(
                        str(k) + object_to_string(v)
                        for k, v in kwargs.items()
                    ),
                    u"//".join(
                        str(v.updated)
                        for k, v in kwargs.items() if hasattr(v, "updated")
                    ),
                )
            ).encode("utf-8")).hexdigest()
            flag = key + "flag"

            # If a cached result exists, return it.
            skip_cache_read = kwargs.pop("skip_cache_read", False)
            result = (
                cache.get(key) if
                not skip_cache_read and cache.get(flag)
                else None
            )

            if result:
                return result[0]

            # If no result, generate one. While generating a result,
            # postpone further regenerations to prevent cache stampeding.
            cache.set(flag, True, int(math.log(seconds)))
            result = f(*args, **kwargs)
            cache.set(
                flag,
                True,
                seconds + randint(
                    -int(seconds * expiry_variance),
                    int(seconds * expiry_variance)
                )
            )
            cache.set(key, (result, ), max(seconds * 10, 86400 * 7))
            return result
        return x

    def object_to_string(obj):
        if isinstance(obj, Model):
            object_class = type(obj)
            return ".".join((
                object_class.__module__,
                object_class.__name__,
                obj.pk,
            ))
        else:
            return str(obj)
    return doCache
