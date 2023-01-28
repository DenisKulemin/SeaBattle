"""Module contains methods for automatic generation of API specifications"""
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin  # type: ignore
from flask import Flask


def load_docstrings(spec: APISpec, app: Flask) -> None:
    """
    Method loads endpoint methods docstrings for further parsing.
    Args:
        spec: APISpec object.
        app: Flask application object.
    """

    for view_fn in app.view_functions.values():
        spec.path(view=view_fn)


def get_apispec(app: Flask, api_title: str, api_version: str) -> APISpec:
    """
    Method creates APISpec based on the docstring data of flask endpoints.
    Args:
        app: Flask application object.
        api_title: Title that is used in API spec.
        api_version: Version of API.

    Returns:
        API spec config.
    """
    spec = APISpec(
        title=api_title,
        version=api_version,
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()]
    )
    load_docstrings(spec, app)
    return spec
