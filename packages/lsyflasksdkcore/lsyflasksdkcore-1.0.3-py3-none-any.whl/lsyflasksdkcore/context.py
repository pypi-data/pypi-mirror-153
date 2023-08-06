# -*- coding: utf-8 -*-s

import typing
from decimal import Decimal

from flask import jsonify, json, request
from flask.sessions import SecureCookieSessionInterface

from .schema import Schema
from .serialization import Serialization, SerializationError


class JWTSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        return


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class RequestQuery(object):
    def __init__(self, schema: typing.Type[Schema], many: bool = False, default: dict = None, cover: dict = None):
        """
        :param schema: 序列化类
        :param many: 是否多条记录
        :param default: 为请求数据默认赋值
        :param cover: 覆盖值,对请求的值进行覆盖
        """
        self.schema = schema
        self._data = None
        self._body = None
        self._valid_message = []
        self.default = default
        self.cover = cover
        self.many = many

    @property
    def data(self):
        return self._data

    @property
    def body(self):
        return self._body

    def is_valid(self, is_form=False):
        if is_form:
            body = request.form.to_dict()
        else:
            if request.is_json:
                query = request.get_json()
            else:
                query = json.loads(request.data)
            body = query.get("body", {})

        if self.default:
            for k, v in self.default.items():
                if k not in body:
                    body[k] = v

        if self.cover:
            body.update(self.cover)

        self._body = body
        try:
            self._data = Serialization.load(self.schema(), body, self.many)
        except SerializationError as ex:
            self._valid_message = ex.description_messages()
            return False
        return True

    @property
    def valid_message(self):
        return ','.join(self._valid_message)

    @property
    def valid_message_list(self):
        return self._valid_message


def sresponse(data=None, **kwargs):
    """success response"""
    d = {'code': 200, 'message': '成功', 'data': data, 'error': False}
    d.update(kwargs)
    return jsonify(d)


def eresponse(message, **kwargs):
    """error response"""
    d = {'code': -1, 'message': message, 'data': None, 'error': True}
    d.update(kwargs)
    return jsonify(d)
