from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.argument import Argument
from aasm.intermediate.instruction import ListRead

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_LR(state: State, arg1: str, arg2: str, arg3: str) -> None:
    state.require(
        state.in_action, "Not inside any action.", "LR can be used inside actions."
    )
    dst = Argument(state, arg1)
    list_ = Argument(state, arg2)
    idx = Argument(state, arg3)
    state.require(
        dst.list_read_context(list_, idx),
        "Mismatched types in the list read context.",
        f"ARG1 {dst.explain()}, ARG2 {list_.explain()}, ARG3 {idx.explain()}",
    )

    state.last_action.add_instruction(ListRead(dst, list_, idx))
