from __future__ import annotations

from aasm.preprocessor.preprocessor_item import PreprocessorItem


class Constant(PreprocessorItem):
    def __init__(self, signature: str):
        super().__init__(signature)
        self.name = ""

    def __repr__(self):
        return f"Constant({self.name})"

    def add_definition(self, name: str, value: str):
        self.name = name
        self.value = value

    def expand(self, line: str) -> str:
        tokens = [token.strip() for token in line.strip().replace(",", " ").split()]
        tokens = [self.value if token == self.name else token for token in tokens]
        if len(tokens) < 2:
            return line
        new_line = tokens[0] + " "
        new_line = new_line + " ".join(tok + "," for tok in tokens[1:])
        new_line = new_line.lstrip(",")
        return new_line
