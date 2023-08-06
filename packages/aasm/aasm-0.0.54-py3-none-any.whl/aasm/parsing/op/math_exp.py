from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.argument import Argument
from aasm.intermediate.instruction import Logarithm, Power

if TYPE_CHECKING:
    from aasm.parsing.state import State


def handle_math_exp_statement(
    state: State, op: str, arg1: str, arg2: str, arg3: str
) -> None:
    state.require(
        state.in_action, "Not inside any action", f"{op} can be used inside actions."
    )
    dst = Argument(state, arg1)
    base = Argument(state, arg2)
    arg = Argument(state, arg3)
    state.require(
        dst.math_exponentiation_context(base, arg),
        "Mismatched types in the math exponentiation statement.",
        f"ARG1 {dst.explain()}, ARG2 {base.explain()}, ARG3 {arg.explain()}",
    )

    match op:
        case "LOG":
            state.last_action.add_instruction(Logarithm(dst, base, arg))

        case "POW":
            state.last_action.add_instruction(Power(dst, base, arg))

        case _:
            state.panic(f"Unexpected error: {op} {arg1} {arg2} {arg3}")
