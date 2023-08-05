#    Copyright 2022 @jack-tee
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import dataclasses
import importlib
from typing import List

import yaml

from .column import Column
from .target import Target
from .utils import get_parts


class BaseFactory:
    """Base class creating entities based on input dicts"""
    class_ = None
    error_class = None
    id_key: str
    type_key: str
    short_key: str
    short_skip_fields: str
    import_path: str | None = None

    @classmethod
    def get_subclass(cls, key: str):
        if cls.import_path:
            importlib.import_module(cls.import_path)
        for c in cls.class_.__subclasses__():
            if c.__name__ == key:
                return c
        raise NotImplementedError(
            f"Could not find class named [{key}] in subclasses")

    @classmethod
    def parse_from_yaml(cls, yaml_str):
        """For testing"""
        conf = yaml.safe_load(yaml_str)
        return cls.parse(conf)

    @classmethod
    def parse(cls, conf: dict):
        """Read the column configuration and return the specified column type."""

        if cls.short_key and conf.get(cls.short_key):
            type_ = conf.get(cls.short_key).split()[1]

        elif conf.get(cls.type_key):
            type_ = conf.get(cls.type_key)

        else:
            raise NotImplementedError(
                f"[{conf.get('name')}]. Could not determine type. Missing key {cls.type_key}"
            )

        c = cls.get_subclass(type_)

        return cls.build(c, conf)

    @classmethod
    def build(cls, c: type, conf: dict):
        """Build the column type from the provided column configuration."""

        if conf.get(cls.type_key):
            pass

        elif cls.short_key and conf.get(cls.short_key):
            parts = get_parts(conf.get(cls.short_key))
            fields = [
                f for f in dataclasses.fields(c)
                if f.name not in cls.short_skip_fields and f.type != List[any]
            ]
            for f, conf_part in zip(fields, parts):
                if f.type != any:
                    conf[f.name] = f.type(conf_part.strip())
                else:
                    conf[f.name] = conf_part.strip()

            del conf[cls.short_key]

        try:
            if conf.get("columns"):
                sub_columns = []
                for elem in conf.get("columns"):

                    sub_columns.append(cls.parse(elem))

                conf["columns"] = sub_columns

            return c(**conf)
        except Exception as e:

            raise cls.error_class(
                f"Error: {cls.class_.__name__} [{conf[cls.id_key]}]. {e}")


class ColumnParsingException(Exception):
    pass


class ColumnFactory(BaseFactory):
    class_ = Column
    error_class = ColumnParsingException
    id_key: str = "name"
    type_key: str = "column_type"
    short_key: str = "col"
    short_skip_fields: List[str] = [
        "null_percentage", "id", "decimal_places", "output_type", "date_format"
    ]
    import_path: str | None = None


class TargetParsingException(Exception):
    pass


class TargetFactory(BaseFactory):
    class_ = Target
    error_class = TargetParsingException
    id_key: str = "target"
    type_key: str = "target"
    short_key: str = None
    short_skip_fields: List[str] = []
    import_path: str | None = None
