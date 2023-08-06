from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List


class MessageParam:
    def __init__(self, name: str):
        self.name: str = name
        self.value: str = ""
        self.is_value_set: bool = False

    def set_value(self, value: str) -> None:
        self.is_value_set = True
        self.value = value

    def print(self) -> None:
        print(f"MessageParam {self.name} = {self.value}")


class FloatParam(MessageParam):
    def __init__(self, name: str):
        super().__init__(name)

    def print(self) -> None:
        print(f"MessageFloatParam")
        super().print()


class ConnectionParam(MessageParam):
    def __init__(self, name: str):
        super().__init__(name)

    def print(self) -> None:
        print(f"MessageConnectionParam")
        super().print()


class Message:
    RESERVED_CONNECTION_PARAMS = ["sender"]
    RESERVED_TYPE_PARAMS = ["type", "performative"]

    def __init__(self, msg_type: str, msg_performative: str):
        self.type: str = msg_type
        self.performative: str = msg_performative
        self.float_params: Dict[str, FloatParam] = {}
        self.connection_params: Dict[str, MessageParam] = {}

    @property
    def param_names(self) -> List[str]:
        return [
            *Message.RESERVED_CONNECTION_PARAMS,
            *Message.RESERVED_TYPE_PARAMS,
            *list(self.float_params),
            *list(self.connection_params),
        ]

    @property
    def unset_params(self) -> List[str]:
        unset_params: List[str] = []

        for name, float_param in self.float_params.items():
            if not float_param.is_value_set:
                unset_params.append(name)

        for name, connection_param in self.connection_params.items():
            if not connection_param.is_value_set:
                unset_params.append(name)

        return unset_params

    def are_all_params_set(self) -> bool:
        return all(
            [float_param.is_value_set for float_param in self.float_params.values()]
            + [
                connection_param.is_value_set
                for connection_param in self.connection_params.values()
            ]
        )

    def param_exists(self, name: str) -> bool:
        return name in self.param_names

    def add_float(self, float_param: FloatParam) -> None:
        self.float_params[float_param.name] = float_param

    def add_connection(self, connection_param: ConnectionParam) -> None:
        self.connection_params[connection_param.name] = connection_param

    def print(self) -> None:
        print(f"Message {self.type}/{self.performative}")
        for float_param in self.float_params.values():
            float_param.print()
        for connection_param in self.connection_params.values():
            connection_param.print()
