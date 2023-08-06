__all__ = ["RedisPal"]

import pickle
from time import time
from typing import Union
import dill
import redis
from redis_pal.exceptions import SerializationError, DeserializationError


class RedisPal(redis.Redis):
    """
    RedisPal helps you store data on Redis
    without worrying about serialization
    stuff. Besides that, it also stores
    timestamps for last changes so you can
    check that whenever you want.

    You can use this as a key-value data
    structure using "get" and "set"
    methods.

    This class inherits from redis.Redis
    and the main difference is that it
    handles serialization and deserialization
    of objects so you can set anything to
    a key.
    """

    def __repr__(self) -> str:
        """
        Representation of this object
        """

        return "<RedisPal <pool={}>>".format(self.connection_pool)

    def __str__(self) -> str:
        """
        Representation of this object
        """

        return self.__repr__()

    @classmethod
    def _serialize(cls, o: object) -> bytes:
        try:
            return pickle.dumps(o)
        except Exception:
            try:
                return dill.dumps(o)
            except:
                raise SerializationError(
                    "Failed to serialize object {} of type {}".format(o, type(o)))

    @classmethod
    def _deserialize(cls, e: Union[str, int, float, bytes]) -> object:
        if e is None:
            return None
        try:
            return pickle.loads(e)
        except:
            try:
                return dill.loads(e)
            except:
                raise DeserializationError(
                    "Failed to deserialize {}".format(e))

    def set(self, key, value, *args, **kwargs) -> bool:
        _ser = self._serialize(value)
        _a = super(RedisPal, self).set(
            name="{}_timestamp".format(key), value=time(), *args, **kwargs)
        _b = super(RedisPal, self).set(
            name=key, value=_ser, *args, **kwargs
        )
        return all([_a, _b])

    def get(self, key, *args, **kwargs) -> object:
        return self._deserialize(super(RedisPal, self).get(name=key, *args, **kwargs))

    def get_with_timestamp(self, key, *args, **kwargs) -> dict:
        last_modified = super(RedisPal, self).get(
            name="{}_timestamp".format(key), *args, **kwargs)
        return {
            "value": self._deserialize(super(RedisPal, self).get(name=key, *args, **kwargs)),
            "last_modified": float(last_modified) if last_modified else 0
        }
