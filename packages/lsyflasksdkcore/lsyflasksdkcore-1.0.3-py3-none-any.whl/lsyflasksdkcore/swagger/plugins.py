from apispec import BasePlugin
from apispec.ext.marshmallow import resolve_schema_cls
from apispec.yaml_utils import load_operations_from_docstring
from marshmallow import Schema, fields


class DocPlugin(BasePlugin):
    def __init__(self):
        self.openapi_major_version = None

    def init_spec(self, spec):
        super(DocPlugin, self).init_spec(spec)

    def operation_helper(self, path=None, operations=None, **kwargs):
        func = kwargs["view"]

        print(func.__doc__)
        doc_operations = load_operations_from_docstring(func.__doc__)
        operations.update(doc_operations)


class MyPlugin(BasePlugin):
    def __init__(self):
        self.openapi_major_version = None

    def init_spec(self, spec):
        super(MyPlugin, self).init_spec(spec)
        self.openapi_major_version = spec.openapi_version.major

    def operation_helper(self, path=None, operations=None, **kwargs):
        for operation in operations.values():
            if not isinstance(operation, dict):
                continue

            # requestBody
            for content in operation["requestBody"]["content"].values():
                if "schema" in content:
                    schema = content["schema"]
                    if isinstance(schema, dict):
                        schema_dict = {}
                        for prop_key, prop_value in schema["properties"].items():
                            if prop_key == "body":
                                if isinstance(prop_value, dict):
                                    schema_name = prop_value["items"]
                                    schema_class = resolve_schema_cls(schema_name)
                                    schema_dict["body"] = fields.Nested(schema_class, many=True,
                                                                        description=schema_class.__doc__)
                                else:
                                    schema_class = resolve_schema_cls(prop_value)
                                    schema_dict["body"] = fields.Nested(schema_class, many=False,
                                                                        description=schema_class.__doc__)
                            else:
                                if isinstance(prop_value, dict):
                                    prop_value_type = prop_value["type"]
                                    prop_value_description = prop_value.get("description", None)
                                    prop_value_required = prop_value.get("required", False)

                                    if prop_value_type in ("integer", "long",):
                                        schema_dict[prop_key] = fields.Int(description=prop_value_description,
                                                                           required=prop_value_required)
                                    elif prop_value_type in ("float", "double",):
                                        schema_dict[prop_key] = fields.Float(description=prop_value_description,
                                                                             required=prop_value_required)
                                    elif prop_value_type in ("boolean",):
                                        schema_dict[prop_key] = fields.Boolean(description=prop_value_description,
                                                                               required=prop_value_required)
                                    else:
                                        schema_dict[prop_key] = fields.Str(description=prop_value_description,
                                                                           required=prop_value_required)
                                else:
                                    schema_class = resolve_schema_cls(prop_value)
                                    schema_dict[prop_key] = fields.Nested(schema_class, many=False)
                        content["schema"] = Schema.from_dict(schema_dict)
                    else:
                        schema_class = resolve_schema_cls(prop_value)
                        content["schema"] = Schema.from_dict({
                            "timestamp": fields.Str(),
                            "body": fields.Nested(schema_class)
                        })

            # responses
            for response in operation.get("responses", {}).values():
                for content in response["content"].values():
                    if "schema" in content:
                        schema = content["schema"]
                        if isinstance(schema, dict):
                            schema_dict = {}
                            for prop_key, prop_value in schema["properties"].items():
                                if prop_key == "data":
                                    if isinstance(prop_value, dict):
                                        schema_name = prop_value["items"]
                                        schema_class = resolve_schema_cls(schema_name)
                                        schema_dict["data"] = fields.Nested(schema_class, many=True,
                                                                            description=schema_class.__doc__)
                                    else:
                                        schema_class = resolve_schema_cls(prop_value)
                                        schema_dict["data"] = fields.Nested(schema_class, many=False,
                                                                            description=schema_class.__doc__)
                                else:
                                    if isinstance(prop_value, dict):
                                        prop_value_type = prop_value["type"]
                                        prop_value_description = prop_value.get("description", None)
                                        prop_value_required = prop_value.get("required", False)

                                        if prop_value_type in ("integer", "long",):
                                            schema_dict[prop_key] = fields.Int(description=prop_value_description,
                                                                               required=prop_value_required)
                                        elif prop_value_type in ("float", "double",):
                                            schema_dict[prop_key] = fields.Float(description=prop_value_description,
                                                                                 required=prop_value_required)
                                        elif prop_value_type in ("boolean",):
                                            schema_dict[prop_key] = fields.Boolean(description=prop_value_description,
                                                                                   required=prop_value_required)
                                        else:
                                            schema_dict[prop_key] = fields.Str(description=prop_value_description,
                                                                               required=prop_value_required)
                                    else:
                                        schema_class = resolve_schema_cls(prop_value)
                                        schema_dict[prop_key] = fields.Nested(schema_class, many=False)
                            content["schema"] = Schema.from_dict(schema_dict)
                        else:
                            schema_class = resolve_schema_cls(prop_value)
                            content["schema"] = Schema.from_dict({
                                "message": fields.Str(),
                                "error": fields.Str(),
                                "data": fields.Nested(schema_class),
                                "code": fields.Int(),
                                "total": fields.Int()
                            })
