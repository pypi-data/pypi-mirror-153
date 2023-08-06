from __future__ import annotations

import re
from typing import List

from aasm.preprocessor.preprocessor_item import PreprocessorItem


class Macro(PreprocessorItem):
    def __init__(self, signature):
        super().__init__(signature)
        self.lines = []
        self.argument_regexes = []
        self.name = ""
        self.expand_len = 0

    def __repr__(self):
        return f"Macro({self.name})"

    def expand(self, macro_args: List[str]) -> List[str]:
        expanded = []
        macro_args = [" " + arg + "," for arg in macro_args]
        substitutions = list(zip(macro_args, self.argument_regexes))
        for line in self.lines:
            expand_line = line
            for sub in substitutions:
                # expand_line = expand_line.replace(sub[1], sub[0])
                expand_line = re.sub(sub[1], sub[0], expand_line)
                expand_line = expand_line.rstrip(",")
            expanded.append(expand_line)
        return expanded

    def _create_regex(self, name: str) -> str:
        return f"[\\s,]{name}\\s*,?"

    def add_definition(self, definition: List[str]):
        # definition = [token for token in definition if token != '']
        self.name = definition[0]
        self.argument_regexes = [self._create_regex(arg) for arg in definition[1:]]

    def add_line(self, line: str):
        self.lines.append(line)
        self.expand_len += 1
