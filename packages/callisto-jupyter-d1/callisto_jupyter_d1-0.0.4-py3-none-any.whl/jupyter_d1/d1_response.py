import json
import typing
import uuid
from datetime import date, datetime

from starlette.responses import JSONResponse


def d1_pairs_hook(pairs):
    """ 
    To be used with json.load(s), attempts to convert any
    attribute with a name ending in 'uuid' into a UUID
    object.  The conversion may fail, in which case the
    value silently passes through.
    """
    ret_dict = {}
    for pair in pairs:
        (key, value) = pair
        if key.endswith("uuid"):
            try:
                value = uuid.UUID(value)
            except ValueError:
                pass
            except TypeError:
                pass
        ret_dict[key] = value
    return ret_dict


class D1Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class D1Response(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=D1Encoder,
        ).encode("utf-8")
