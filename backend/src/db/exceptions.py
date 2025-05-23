from typing import Any


class ModelNotFoundException(Exception):
    def __init__(self, table: str, args: Any) -> None:
        self.table = table
        self.args = args

    def __str__(self) -> str:
        return f"Entity from {self.table} with args {self.args} not found"


class ModelConflictException(Exception):
    def __init__(self, table: str, args: Any) -> None:
        self.table = table
        self.args = args

    def __str__(self) -> str:
        return f"Entity {self.table} with args {self.args} cannot be created"

