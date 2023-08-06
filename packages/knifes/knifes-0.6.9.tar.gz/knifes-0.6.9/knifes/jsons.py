import json
import datetime
from . import times
import decimal
import uuid
import enum


# object encode
class ObjectEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return times.to_timestamp(o, unit='millisecond')
        elif isinstance(o, (decimal.Decimal, uuid.UUID, enum.Enum)):
            return str(o)
        elif isinstance(o, set):
            return list(o)
        else:
            d = o.__dict__.copy()
            for key, value in o.__class__.__dict__.items():
                if isinstance(value, property):
                    d[key] = getattr(o, key)
            return d


# obj to json
def to_json(obj):
    return json.dumps(obj, cls=ObjectEncoder)