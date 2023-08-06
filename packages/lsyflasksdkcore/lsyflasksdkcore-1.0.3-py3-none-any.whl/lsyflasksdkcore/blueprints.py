# -*- coding: utf-8 -*-

import functools

from flask import current_app, Blueprint as BaseBlueprint
from flask_login import current_user

AUTH_ADD_FUNC_CODE = "add"
AUTH_EDIT_FUNC_CODE = "edit"
AUTH_DELETE_FUNC_CODE = "delete"
AUTH_EXPORT_FUNC_CODE = "export"


class AuthGrant(object):
    """ 权限认证
    """

    def __init__(self, module_code, import_name):
        self.module_code = module_code
        self.import_name = import_name

    def _verify_authorization(self, func_code):
        """
        验证授权
        :param func_code: 功能编码
        :return:
        """

        # 判断用户是否登录
        if not current_user.is_authenticated:
            return False

        # 判断用户是否有访问模块和对应功能的权限

        print(self.module_code)
        print(func_code)
        return True

    def _grant(self, func, func_code):
        @functools.wraps(func)
        def __grant(*args, **kwargs):
            if not self._verify_authorization(func_code):
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)

        return __grant

    def grant(self, func_code):
        """自定义授权"""

        def _wrap(func):
            return self._grant(func, func_code)

        return _wrap

    def grant_view(self, func):
        """查看授权"""
        return self._grant(func, None)

    def grant_add(self, func):
        """新增授权"""
        return self._grant(func, AUTH_ADD_FUNC_CODE)

    def grant_edit(self, func):
        """编辑授权"""
        return self._grant(func, AUTH_EDIT_FUNC_CODE)

    def grant_delete(self, func):
        """删除授权"""
        return self._grant(func, AUTH_DELETE_FUNC_CODE)

    def grant_export(self, func):
        """导出授权"""
        return self._grant(func, AUTH_EXPORT_FUNC_CODE)


class Blueprint(BaseBlueprint):
    def __init__(self, name, import_name, module_name=None):
        if not module_name:
            module_name = name
        self.auth = AuthGrant(module_name, import_name)
        BaseBlueprint.__init__(self, name, import_name)
