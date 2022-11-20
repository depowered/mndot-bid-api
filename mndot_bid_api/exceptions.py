from fastapi import HTTPException, status


class RecordNotFoundError(Exception):
    pass


class RecordAlreadyExistsError(Exception):
    pass


class InvalidBidError(Exception):
    pass


def raise_http_404(model_name: str, id: int, exc: Exception) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{model_name} at ID {id} not found",
    ) from exc


def raise_http_404_query(model_name: str, exc: Exception) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No {model_name} records found matching the provided query parameters",
    ) from exc


def raise_http_303(model_name: str, id: int, exc: Exception) -> None:
    raise HTTPException(
        status_code=status.HTTP_303_SEE_OTHER,
        detail=f"{model_name} already exists at ID {id}",
    ) from exc
