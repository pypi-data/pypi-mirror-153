from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.argument import Argument
from aasm.intermediate.instruction import Modulo

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_MOD(state: State, arg1: str, arg2: str, arg3: str) -> None:
    state.require(
        state.in_action, "Not inside any action", f"MOD can be used inside actions."
    )
    dst = Argument(state, arg1)
    dividend = Argument(state, arg2)
    divisor = Argument(state, arg3)
    state.require(
        dst.math_modulo_context(dividend, divisor),
        "Mismatched types in the math modulo statement.",
        f"ARG1 {dst.explain()}, ARG2 {dividend.explain()}, ARG3 {divisor.explain()}",
    )

    state.last_action.add_instruction(Modulo(dst, dividend, divisor))
