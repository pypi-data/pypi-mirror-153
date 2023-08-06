import six
import yaml


def get_fun_key(fun):
    """
    获取函数得key
    :param fun: 函数
    :return:
    """
    return id(fun)


def isschema(prop_type):
    """
    判断属性的类型是否为Schema
    :param prop_type:
    :return:
    """
    return prop_type.rfind("Schema") != -1


def gen_property(prop_name, prop_type, required=True, prop_desc="", many=True):
    """
    生成属性
    :param prop_name: 属性名称
    :param prop_type: 属性类型
    :param required: 是否必填
    :param prop_desc: 描述
    :param many: 是否数组
    :return:
    """
    if isschema(prop_type):
        if many:
            p = {"type": "array", "items": prop_type}
            if required:
                p["required"] = required

            if prop_desc:
                p["description"] = prop_desc

            return p
        else:
            return prop_type
    else:
        if many:
            p = {"type": "array", "items": prop_type}
        else:
            p = {"type": prop_type}
        if required:
            p["required"] = required

        if prop_desc:
            p["description"] = prop_desc
        return p


class SwaggerDoc(object):
    """ This class is used to control the SwaggerDoc integration to one or more Flask applications.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

        self._handlers = []

        self._req_props = {}
        self._rsp_props = {}

    def init_app(self, app):
        if not self.app:
            self.app = app

    @property
    def handlers(self):
        return self._handlers

    def _add_req_prop(self, fun, prop_name, prop_type, required=True, prop_desc="", many=True):
        """
        add requestBody properties
        :param fun: view fun
        :param prop_name: 属性名称
        :param prop_type: 属性类型，可以是Schema也可以是简单类型，比如integer等。
        :param required: 是否必填
        :param prop_desc: 属性描述
        :param many: 是否是数组
        :return:
        """
        fun_id = get_fun_key(fun)
        props = self._req_props.get(fun_id, [])

        p = gen_property(prop_name, prop_type, required, prop_desc, many)
        props.append({prop_name: p})
        self._req_props.update({fun_id: props})

    def _add_rsp_prop(self, fun, prop_name, prop_type, required=True, prop_desc="", many=True):
        """
        add response properties
        :param fun: view fun
        :param prop_name: 属性名称
        :param prop_type: 属性类型，可以是Schema也可以是简单类型，比如integer等。
        :param required: 是否必填
        :param prop_desc: 属性描述
        :param many: 是否是数组
        :return:
        """
        fun_id = id(fun)
        props = self._rsp_props.get(fun_id, [])

        p = gen_property(prop_name, prop_type, required, prop_desc, many)
        props.append({prop_name: p})
        self._rsp_props.update({fun_id: props})

    def _swagger_doc_yaml(self, fun_id, fun_doc, method, tag):
        add_req_props = self._req_props.get(fun_id, None)
        add_rsp_props = self._rsp_props.get(fun_id, None)

        req_props = {
            "timestamp": {"type": "integer", "required": True, "description": "时间戳"}
        }

        rsp_props = {
            "code": {"type": "integer", "description": "http code"},
            "error": {"type": "boolean", "description": "error"},
            "message": {"type": "string", "description": "message"}
        }

        req_requireds = []
        rsp_requireds = []

        if add_req_props:
            for item in add_req_props:
                req_props.update(item)

        if add_rsp_props:
            for item in add_rsp_props:
                rsp_props.update(item)

        for key, value in req_props.items():
            if isinstance(value, dict) and value.get("required", False):
                del value['required']
                req_requireds.append(key)

        for key, value in rsp_props.items():
            if isinstance(value, dict) and value.get("required", False):
                del value['required']
                rsp_requireds.append(key)

        doc_obj = {
            method: {
                "summary": fun_doc,
                "tags": [tag],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": req_requireds,
                                "properties": req_props
                            }
                        }
                    }
                },
                'responses': {
                    200: {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": rsp_requireds,
                                    "properties": rsp_props
                                }
                            }
                        }
                    }
                }
            }
        }
        return yaml.dump(doc_obj)

    def post(self, tag, body_schema="string", data_schema="string"):
        """ swagger post doc
        :param tag: 标签
        :param body_schema: 请求body schema
        :param data_schema: 响应data schema
        :return:
        """

        def doc(fun):
            self._handlers.append(fun)

            # 如果body_schema与data_schema是字符串表示是many=false,反之many=true
            if isinstance(body_schema, six.text_type):
                self._add_req_prop(fun, "body", body_schema, False, "", False)
            else:
                self._add_req_prop(fun, "body", body_schema[0], False, "", True)

            if isinstance(data_schema, six.text_type):
                self._add_rsp_prop(fun, "data", data_schema, False, "", False)
            else:
                self._add_rsp_prop(fun, "data", data_schema[0], False, "", True)

            fun_id = get_fun_key(fun)
            fun_doc = fun.__doc__ or fun.__name__

            swagger_doc_yaml = self._swagger_doc_yaml(fun_id, fun_doc, "post", tag)
            fun.__doc__ = fun_doc.replace(" ", "") + "\n---\n" + swagger_doc_yaml
            return fun

        return doc

    def pager(self):
        def doc(fun):
            self._add_rsp_prop(fun, "total", "integer", True, "页大", False)
            return fun

        return doc

    def post_pager(self):
        pass

    def req_body(self, schema, many=False):
        def prop(fun):
            self._add_req_prop(fun, "body", schema, True, "", many)
            return fun

        return prop

    def rsp_data(self, schema, many=False):
        def prop(fun):
            self._add_rsp_prop(fun, "data", schema, True, "", many)
            return fun

        return prop

    def add_req_body_prop(self, schema, many=False):
        pass

    def add_req_schema_prop(self, prop_name, schema):
        pass

    @staticmethod
    def add_req_integer_prop(prop_name, prop_type, prop_desc):
        def prop(fun):
            return fun

        return prop
