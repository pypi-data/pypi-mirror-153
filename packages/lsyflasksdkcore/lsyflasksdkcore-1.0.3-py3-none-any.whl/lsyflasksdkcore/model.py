# -*- coding: utf-8 -*-
import functools
from typing import TypeVar, Generic, List, Dict

from lsyflasksdkcore.linq import LinqQuery
from lsyflasksdkcore.utils.lazy import lazy_property
from .serialization import Serialization, AutoClass, SerializationError

T = TypeVar("T")


class DBResult(Generic[T]):
    def __init__(self, data, schema_class, many=False):
        self.original_data = data
        self.schema_class = schema_class
        self.many = many

    @lazy_property
    def shema_instance(self):
        return self.schema_class()

    @lazy_property
    def json(self):
        if not self.original_data:
            return [] if self.many else {}

        try:
            return Serialization.dump(self.shema_instance, self.original_data, self.many)
        except SerializationError as ex:
            raise ex

    @lazy_property
    def data(self):
        json_data = self.json
        if not json_data:
            return [] if self.many else {}

        try:
            return Serialization.load(self.shema_instance, json_data, self.many)
        except SerializationError as ex:
            raise ex

    def to_json(self) -> Dict:
        return self.json

    def to_data(self) -> T:
        _data = self.data
        if self.many and _data:
            return _data[0]
        return self.data

    def to_list(self) -> List[T]:
        _data = self.data
        if not self.many and _data:
            return [_data]
        return self.data

    def to_query(self) -> LinqQuery[T]:
        return LinqQuery(self.data)


class Model(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not self.app:
            self.app = app

    @staticmethod
    def entity(schema_class):
        def _query(func):
            @functools.wraps(func)
            def __query(*args, **kwargs) -> DBResult:
                result = func(*args, **kwargs)
                dbr = DBResult(result, schema_class, False)
                return dbr

            return __query

        return _query

    @staticmethod
    def list(schema_class):
        def _query(func):
            @functools.wraps(func)
            def __query(*args, **kwargs):
                result = func(*args, **kwargs)
                dbr = DBResult(result, schema_class, True)
                return dbr

            return __query

        return _query

    @staticmethod
    def pager(schema_class):
        def _pager(func):
            @functools.wraps(func)
            def __pager(*args, **kwargs):
                result, count = func(*args, **kwargs)
                dbr = DBResult(result, schema_class, True)
                return dbr, count

            return __pager

        return _pager


class PagerQuery(AutoClass):
    def __init__(self):
        self.page = 1
        self.rows = 20
        self.offset = 0


class DBRef(AutoClass):
    def __init__(self):
        self.ref_desc = ""
        self.ref_code = ""
        self.ref_count = ""

    def withDesc(self, desc: str):
        self.ref_desc = desc
        return self

    def withCode(self, code: str):
        self.ref_code = code
        return self

    def withCount(self, count: int):
        self.ref_count = count
        return self
