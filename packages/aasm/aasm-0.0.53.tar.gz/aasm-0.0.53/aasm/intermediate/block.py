from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from aasm.intermediate.declaration import Declaration
    from aasm.intermediate.instruction import Instruction


class Declarations:
    def __init__(
        self,
        float_names: List[str] | None = None,
        connection_names: List[str] | None = None,
    ):
        if float_names:
            self.float_names: List[str] = float_names
        else:
            self.float_names: List[str] = []

        if connection_names:
            self.connection_names: List[str] = connection_names
        else:
            self.connection_names: List[str] = []

    def add_float_name(self, name: str) -> None:
        self.float_names.append(name)

    def is_float_name(self, name: str) -> bool:
        return name in self.float_names

    def add_connection_name(self, name: str) -> None:
        self.connection_names.append(name)

    def is_connection_name(self, name: str) -> bool:
        return name in self.connection_names

    def get_declared_names(self) -> List[str]:
        return [*self.float_names, *self.connection_names]

    def get_copy(self) -> Declarations:
        return Declarations(list(self.float_names), list(self.connection_names))

    def print(self) -> None:
        print("Declarations")
        print(f"float_names = {self.float_names}")
        print(f"connection_names = {self.connection_names}")


class Block:
    def __init__(self, parent_declarations: Declarations):
        self.statements: List[Declaration | Instruction | Block] = []
        self._declarations: Declarations = parent_declarations.get_copy()

    @property
    def declared_names_in_scope(self) -> List[str]:
        return self._declarations.get_declared_names()

    @property
    def get_declarations(self) -> Declarations:
        return self._declarations

    def is_declared_float(self, name: str) -> bool:
        return self._declarations.is_float_name(name)

    def is_declared_connection(self, name: str) -> bool:
        return self._declarations.is_connection_name(name)

    def add_float_declaration(self, declaration: Declaration) -> None:
        self._declarations.add_float_name(declaration.name)
        self.statements.append(declaration)

    def add_connection_declaration(self, declaration: Declaration) -> None:
        self._declarations.add_connection_name(declaration.name)
        self.statements.append(declaration)

    def add_statement(self, statement: Instruction | Block) -> None:
        self.statements.append(statement)

    def print(self) -> None:
        print(f"Block")
        print(f"Names in scope")
        self._declarations.print()
        for instruction in self.statements:
            instruction.print()
        print("(EndBlock)")
