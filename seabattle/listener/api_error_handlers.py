"""Module contains error handlers that works on API level. They catch api, validation and application errors."""
import ast
import re
import traceback
from typing import Tuple, Dict, Any
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from seabattle.helpers.constants import StatusCode, FRONT_Y_COORDINATE
from seabattle.helpers.logger import API_LOGGER


def handle_validation_error(error: ValidationError) -> Tuple[Dict[str, Any], int]:
    """
    Method handles all validation errors.
    Args:
        error: Validation error from marshmallow.

    Returns:
        tuple: Dictionary whit validation error information and status code.
    """
    response = {"errors": error.messages,
                "statusCode": StatusCode.VALIDATION_FAILED.value,
                "message": "Validation failed."}
    API_LOGGER.error(response)
    return response, StatusCode.VALIDATION_FAILED.value


def handle_api_error(error: HTTPException) -> Tuple[Dict[str, Any], int]:
    """
    Method handles all API errors.
    Args:
        error: API error.

    Returns:
        tuple: Dictionary whit API error information and status code.
    """
    response = {"statusCode": error.code,
                "message": error.description,
                "hint": error.args[0] if error.args else ""}
    API_LOGGER.error(response)
    return response, error.code if error.code is not None else StatusCode.BAD_REQUEST.value


def handle_application_error(error: Exception) -> Tuple[Dict[str, Any], int]:
    """
    Method handles all application errors.
    Args:
        error: Application error.

    Returns:
        tuple: Dictionary whit application error information and status code.
    """
    hint = error.args[0]
    coordinates = re.search(r"\[.*?\]", hint)
    coordinate = re.search(r"\(.*?\)", hint)
    while coordinate or coordinates:
        API_LOGGER.error(hint)
        if coordinates:
            API_LOGGER.error(coordinates)
            front_coordinates = [f"{coordinate[0]}{FRONT_Y_COORDINATE[coordinate[1] - 1]}"
                                 for coordinate in ast.literal_eval(coordinates.group(0))]
            hint = hint.replace(coordinates.group(0), ", ".join(front_coordinates))
        elif coordinate:
            API_LOGGER.error(coordinate)
            front_coordinates = [f"{coordinate[0]}{FRONT_Y_COORDINATE[coordinate[1] - 1]}"
                                 for coordinate in [ast.literal_eval(coordinate.group(0))]]
            hint = hint.replace(coordinate.group(0), ", ".join(front_coordinates))
        coordinates = re.search(r"\[.*?\]", hint)
        coordinate = re.search(r"\(.*?\)", hint)

    response = {"statusCode": StatusCode.APPLICATION_ERROR.value,
                "errorCode": error.__class__.__name__,
                "message": "Internal Server Error.",
                "hint": hint}
    API_LOGGER.error(response)
    traceback.print_exc()
    return response, StatusCode.APPLICATION_ERROR.value
