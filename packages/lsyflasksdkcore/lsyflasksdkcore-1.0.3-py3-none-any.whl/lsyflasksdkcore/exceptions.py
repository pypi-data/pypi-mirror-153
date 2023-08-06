# -*- coding: utf-8 -*-


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['code'] = -1
        rv['data'] = None
        rv['error'] = True
        return rv


class ExcelExportError(Exception):
    pass


class ConfigError(Exception):
    pass


class DBError(Exception):
    pass


class DBRefError(DBError):
    """数据关联错误。"""

    @property
    def message(self):
        ref = self.args[0]
        if isinstance(ref, dict):
            return '关联数据"%(ref_desc)s", %(ref_count)d条' % {'ref_desc': ref['ref_desc'], 'ref_count': ref['ref_count']}
        else:
            return '关联数据"%(ref_desc)s", %(ref_count)d条' % {'ref_desc': ref.ref_desc, 'ref_count': ref.ref_count}


class ImportDataError(Exception):
    """导入数据错误"""

    @property
    def message(self):
        return self.args[0]

    @property
    def excel_errors(self):
        return self.args[1]


class PermissionError(Exception):
    """权限异常"""
    pass


class AuthenticateError(Exception):
    """用户认证错误"""
    pass


class MarshmallowLoadError(Exception):
    pass


class JwtTokenError(Exception):
    pass
