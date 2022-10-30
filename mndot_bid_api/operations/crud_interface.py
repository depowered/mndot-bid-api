from typing import Any, Protocol

RecordDict = dict[str, Any]


class RecordNotFoundException(Exception):
    pass


class RecordAlreadyExistsException(Exception):
    pass


class CRUDInterface(Protocol):
    def read_all(self) -> list[RecordDict]:
        ...

    def read_by_id(self, id: int) -> RecordDict:
        ...

    def create(self, data: RecordDict) -> RecordDict:
        ...

    def update(self, id: int, data: RecordDict) -> RecordDict:
        ...

    def delete(self, id: int) -> None:
        ...
