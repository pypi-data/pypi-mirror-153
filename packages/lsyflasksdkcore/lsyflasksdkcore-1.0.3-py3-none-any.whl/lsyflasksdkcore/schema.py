# -*- coding: utf-8 -*-
import typing
from typing import List

from marshmallow import Schema as BaseSchema, fields, post_load, pre_load, ValidationError

from .model import DBRef


class Schema(BaseSchema):
    def handle_error(self, error: ValidationError, data: typing.Any, *, many: bool, **kwargs):
        messages = error.normalized_messages()
        new_messages = {}
        _fields = self.fields
        if many:
            for index, row_err in messages.items():
                new_msg = {}
                for field_name, err in row_err.items():
                    field = _fields.get(field_name)
                    description = field.metadata.get("description", field_name)
                    new_msg.update({field_name: (description, err)})
                new_messages.update({index: new_msg})
        else:
            for field_name, err in messages.items():
                field = _fields.get(field_name)
                field_description = field.metadata.get("description", field.name)
                new_messages.update({field_name: (field_description, err)})
        error.messages = new_messages


fields.Field.default_error_messages = {
    "required": "缺少必要数据",
    "null": "数据不能为空",
    "validator_failed": "非法数据",
}

fields.Str.default_error_messages = {
    'invalid': "不是合法文本"
}

fields.Int.default_error_messages = {
    "invalid": "不是合法整数"
}

fields.Number.default_error_messages = {
    "invalid": "不是合法数字"
}

fields.Boolean.default_error_messages = {
    "invalid": "不是合法布尔值"
}


class PkQuery(object):
    def __init__(self, id):
        self.id = id


class PksQuery(object):
    def __init__(self, id):
        self.ids = id


class UnionkeyQuery(object):
    def __init__(self, id: str = ""):
        self.id = id
        self.keys = []

    def get_keys(self, split_str: str = "|") -> List[str]:
        self.keys.extend(self.id.split(split_str))
        return self.keys

    def put_key(self, key: str):
        self.keys.append(str(key))
        return self

    def join(self, split_str: str = "|") -> str:
        return split_str.join(self.keys)


class UnionkeysQuery(object):
    def __init__(self, id: str):
        self.ids = id

    def get_unionkeys(self) -> List[UnionkeyQuery]:
        return [UnionkeyQuery(item) for item in self.ids]


class PkQuerySchema(Schema):
    id = fields.Str(required=True, error_messages={"required": "id不能为空"})

    @post_load
    def make(self, data, **kwargs):
        return PkQuery(**data)


class PksQuerySchema(Schema):
    id = fields.List(fields.Str())

    @post_load
    def make(self, data, **kwargs):
        return PksQuery(**data)


class UnionkeyQuerySchema(Schema):
    """联合主键query"""
    id = fields.Str(required=True, error_messages={"required": "id不能为空,"}, description="联合主键用|组合")

    @post_load
    def make(self, data, **kwargs):
        return UnionkeyQuery(**data)


class UnionkeysQuerySchema(Schema):
    """联合主键列表query"""
    id = fields.List(fields.Str())

    @post_load
    def make(self, data, **kwargs):
        return UnionkeysQuery(**data)


class PagerQuerySchema(Schema):
    page = fields.Int(required=True, error_messages={"required": "页码不能为空"})
    rows = fields.Int(required=True, error_messages={"required": "分页大小不能为空"})
    offset = fields.Int()

    @pre_load
    def slugify(self, data, **kwargs):
        data['offset'] = data.get('page', 0) * data.get('rows', 20)
        return data


class DBRefSchema(Schema):
    ref_desc = fields.Str()
    ref_code = fields.Str()
    ref_count = fields.Int()

    @post_load
    def make(self, data, **kwargs):
        return DBRef().__fill__(**data)
