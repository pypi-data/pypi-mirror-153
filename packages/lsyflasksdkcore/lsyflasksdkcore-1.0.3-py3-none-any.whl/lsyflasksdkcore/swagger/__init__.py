import json

from apispec import APISpec
from apispec.exceptions import APISpecError
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from swagger_ui import flask_api_doc

from .doc import SwaggerDoc

doc = SwaggerDoc()


def init_swagger(app):
    doc.init_app(app)


def generate_swagger_ui(app, config_path="./swagger.json", url_prefix='/api/doc', title='API doc'):
    flask_api_doc(app, config_path=config_path, url_prefix=url_prefix, title=title)


def generate_swagger_file(app, title="Linkeddt API", version="1.0.0", description="Documentation for the Linkeddt API"):
    spec = APISpec(
        title=title,
        version=version,
        openapi_version="3.0.2",
        info=dict(description=description),
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        servers=[
            {"url": "http://localhost:8888/", "description": "Local environment", },
        ],
    )

    handlers = doc.handlers

    # Optional security scheme support
    api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
    spec.components.security_scheme("ApiKeyAuth", api_key_scheme)
    # spec.components.schema("GistSchema22", schema=GistSchema1)
    # spec.components.schema("PublicParameter12", schema=PublicParameter)

    # Looping through all the handlers and trying to register them.
    # Handlers without docstring will raise errors. That's why we
    # are catching them silently.
    with app.test_request_context():
        for handler in handlers:
            try:
                spec.path(view=handler)
            except APISpecError as ex:
                pass

    # Write the Swagger file into specified location.
    with open("./swagger.json", "w", encoding="utf-8") as file:
        json.dump(spec.to_dict(), file, ensure_ascii=False, indent=4)


__all__ = ['doc', 'init_swagger', 'generate_swagger_ui', 'generate_swagger_file']
