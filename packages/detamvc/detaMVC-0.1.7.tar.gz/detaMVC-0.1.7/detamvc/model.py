from odetam import DetaModel as odeta_model
from datetime import datetime
import ujson
from typing import List, Optional

DETA_BASIC_TYPES = [dict, list, str, int, float, bool]
DETA_OPTIONAL_TYPES = [Optional[type_] for type_ in DETA_BASIC_TYPES]
DETA_BASIC_LIST_TYPES = [
    List[type_] for type_ in DETA_BASIC_TYPES + DETA_OPTIONAL_TYPES
]
DETA_TYPES = DETA_BASIC_TYPES + DETA_OPTIONAL_TYPES + DETA_BASIC_LIST_TYPES

class DetaModel(odeta_model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # overwriting odetam's implementation
    def _serialize(self, exclude=None):
        if not exclude:
            exclude = []
        as_dict = {}
        for field_name, field in self.__class__.__fields__.items():
            if field_name == "key" and not self.key:
                continue
            if field_name in exclude:
                continue
            # this originally failed when 0, 0.0, or False. Now we only check for None instances
            if getattr(self, field_name, None) is None:
                as_dict[field_name] = None
                continue
            if field.type_ in DETA_TYPES:
                as_dict[field_name] = getattr(self, field_name)
            elif field.type_ == datetime.datetime:
                as_dict[field_name] = getattr(self, field_name).timestamp()
            elif field.type_ == datetime.date:
                as_dict[field_name] = int(getattr(self, field_name).strftime("%Y%m%d"))
            elif field.type_ == datetime.time:
                as_dict[field_name] = int(
                    getattr(self, field_name).strftime("%H%M%S%f")
                )
            else:
                as_dict[field_name] = ujson.loads(self.json(include={field_name}))[
                    field_name
                ]
        return as_dict
    
    # overwriting odetam's implementation
    @classmethod
    def _deserialize(cls, data):
        as_dict = {}
        for field_name, field in cls.__fields__.items():
            # this originally failed when 0, 0.0, or False. Now we only check for None instances
            if field_name not in data:
                continue
            if field.type_ in DETA_TYPES:
                as_dict[field_name] = data[field_name]
            elif field.type_ == datetime.datetime:
                as_dict[field_name] = datetime.datetime.fromtimestamp(data[field_name])
            elif field.type_ == datetime.date:
                as_dict[field_name] = datetime.datetime.strptime(
                    str(data[field_name]), "%Y%m%d"
                ).date()
            elif field.type_ == datetime.time:
                as_dict[field_name] = datetime.datetime.strptime(
                    str(data[field_name]), "%H%M%S%f"
                ).time()
            else:
                try:
                    as_dict[field_name] = ujson.loads(data.get(field_name))
                except (TypeError, ValueError):
                    as_dict[field_name] = data.get(field_name, None)
        return cls.parse_obj(as_dict)