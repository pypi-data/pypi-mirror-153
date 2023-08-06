from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.argument import Argument
from aasm.intermediate.declaration import ConnectionDeclaration, FloatDeclaration
from aasm.utils.validation import is_valid_name, print_invalid_names

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_DECL(state: State, name: str, category: str, value: str) -> None:
    state.require(state.in_action, "Cannot declare variables outside actions.")
    state.require(
        is_valid_name(name),
        f"{name} is not a correct name.",
        f"Names can only contain alphanumeric characters, underscores and cannot be: {print_invalid_names()}.",
    )
    state.require(
        not state.last_agent.param_exists(name),
        f"{name} is already defined in current agent.",
    )
    state.require(
        not state.last_action.is_declaration_in_scope(name),
        f"{name} is already declared in current action scope.",
    )
    name_arg = Argument(state, name)
    value_arg = Argument(state, value)
    state.require(
        name_arg.declaration_context(value_arg),
        "Mismatched types in the declaration context.",
        f"NAME {name_arg.explain()}, VALUE {value_arg.explain()}",
    )

    match category:
        case "float":
            state.last_action.add_float_declaration(
                FloatDeclaration(name_arg, value_arg)
            )

        case "conn":
            state.last_action.add_connection_declaration(
                ConnectionDeclaration(name_arg, value_arg)
            )

        case _:
            state.panic(f"Incorrect declaration: DECL {name} {category} {value}")
