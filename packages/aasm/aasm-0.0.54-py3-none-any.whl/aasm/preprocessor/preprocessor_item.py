from typing import NoReturn


class PreprocessorItem:
    def __init__(self, signature: str):
        self.signature = signature

    def expand(self) -> NoReturn:
        raise NotImplementedError

    def add_definition(self, definition: str) -> NoReturn:
        raise NotImplementedError
