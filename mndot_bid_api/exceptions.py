from fastapi import HTTPException, status
from pandas.errors import ParserError
from pandera.errors import SchemaError


class RecordNotFoundError(Exception):
    pass


class RecordAlreadyExistsError(Exception):
    pass


class InvalidBidError(Exception):
    pass


class ParseAbstractCSVError(Exception):
    pass


def raise_http_404(model_name: str, id: int, exc: Exception) -> None:
    """Raises a fastapi.HTTPException with the following properties
    - status_code: 404 Not Found
    - detail: {model_name} at ID {id} not found"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{model_name} at ID {id} not found",
    ) from exc


def raise_http_404_query(model_name: str, exc: Exception) -> None:
    """Raises a fastapi.HTTPException with the following properties
    - status_code: 404 Not Found
    - detail: No {model_name} records found matching the provided query parameters"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No {model_name} records found matching the provided query parameters",
    ) from exc


def raise_http_303(model_name: str, id: int, exc: Exception) -> None:
    """Raises a fastapi.HTTPException with the following properties
    - status_code: 303 See Other
    - detail: {model_name} already exists at ID {id}"""
    raise HTTPException(
        status_code=status.HTTP_303_SEE_OTHER,
        detail=f"{model_name} already exists at ID {id}",
    ) from exc


def raise_http_400_empty_query() -> None:
    """Raises a fastapi.HTTPException with the following properties
    - status_code: 400 Bad Request
    - detail: Provide at least one query parameter"""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Provide at least one query parameter",
    )


def raise_http_422_schema_error(err: SchemaError):
    detail = {"error": "SchemaError", "message": err.args[0]}
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
    ) from err


def raise_http_422_parser_error(err: ParserError):
    detail = {"error": "ParserError", "message": err.args[0]}
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
    ) from err


def raise_http_422_decode_error(err: UnicodeDecodeError):
    detail = {"error": "UnicodeDecodeError", "message": err.reason}
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
    ) from err


def raise_http_403_forbidden():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
    )
