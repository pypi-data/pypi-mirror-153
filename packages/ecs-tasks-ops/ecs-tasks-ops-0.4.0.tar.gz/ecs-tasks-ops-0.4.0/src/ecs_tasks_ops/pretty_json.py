"""ECS pretty print for json objects."""
import datetime
import json
from json import JSONEncoder


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    """DateTime Encoder for Json."""

    # Override the default method
    def default(self, obj):
        """Default method for encoder."""
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def dumps(obj, indent=2):
    """Print the json object."""
    return json.dumps(obj, indent=indent, cls=DateTimeEncoder)
