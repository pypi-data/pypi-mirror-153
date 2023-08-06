import itertools
from enum import Enum
from get_docker_secret import get_docker_secret


def inherit_attribute(name, f):
    def decorator(cls):
        old_value = getattr(cls, name)
        new_value = f([getattr(base, name) for base in cls.__bases__ if hasattr(base, name)], old_value)
        setattr(cls, name, new_value)
        return cls
    return decorator

def merge_class_val(base_values, my_value = []):
    chain_object = itertools.chain.from_iterable(base_values)
    return list(chain_object) + my_value

def merge_inheritance(name):
    return inherit_attribute(name, merge_class_val)

class CaseInsensitiveEnum(Enum):
    @classmethod
    def _missing_(cls, value):
        if value is None:
            return super()._missing_(cls, value)
        for member in cls:
            if member.name.upper() == value.upper():
                return member
        super()._missing_(cls, value)

IS_PRODUCTION = None
def is_production():
    global IS_PRODUCTION
    if IS_PRODUCTION is None:
        IS_PRODUCTION = get_secret_helper('ENVIRONMENT', 'development') != 'development'
    return IS_PRODUCTION

class MissingSecretException(Exception):
    pass

def get_secret_helper(key, *args, **kwargs):
    s = get_docker_secret(key, default=None)
    if not s:
        if 'default' in kwargs:
            return kwargs['default']
        elif len(args) > 0:
            return args[0]
        elif is_production():
            s = None
        else:
            raise MissingSecretException
    return s

def get_secret_helper_bool(key, default=None, raise_exception=True):
    v = get_secret_helper(key, None)
    if v is None:
        if default is not None or not raise_exception or is_production():
            return default
        else:
            raise MissingSecretException
    else:
        return v.upper() == 'TRUE'
