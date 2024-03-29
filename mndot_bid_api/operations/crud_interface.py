from typing import Any, Protocol

RecordDict = dict[str, Any]


class CRUDInterface(Protocol):
    def read_all(self, limit: int = 0) -> list[RecordDict]:
        ...

    def read_by_id(self, id: int) -> RecordDict:
        ...

    def read_one_by_kwargs(self, **kwargs) -> RecordDict:
        ...

    def read_all_by_kwargs(self, limit: int = 0, **kwargs) -> list[RecordDict]:
        ...

    def create(self, data: RecordDict) -> RecordDict:
        ...

    def update(self, id: int, data: RecordDict) -> RecordDict:
        ...

    def delete(self, id: int) -> None:
        ...
