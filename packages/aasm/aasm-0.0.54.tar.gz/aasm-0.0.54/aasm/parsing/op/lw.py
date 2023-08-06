from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.argument import Argument
from aasm.intermediate.instruction import ListWrite

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_LW(state: State, arg1: str, arg2: str, arg3: str) -> None:
    state.require(
        state.in_action, "Not inside any action.", "LW can be used inside actions."
    )
    list_ = Argument(state, arg1)
    idx = Argument(state, arg2)
    value = Argument(state, arg3)
    state.require(
        list_.list_write_context(idx, value),
        "Mismatched types in the list write context.",
        f"ARG1 {list_.explain()}, ARG2 {idx.explain()}, ARG3 {value.explain()}",
    )

    state.last_action.add_instruction(ListWrite(list_, idx, value))
