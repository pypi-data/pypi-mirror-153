from typing import Any, List, Optional

from declarative_argparse.options.abc import IDeclarativeOption


class FloatDO(IDeclarativeOption):
    def get_value(self) -> Optional[float]:
        o = super().get_value()
        if o is None:
            return None
        return float(o)

    def handle_input(self, arg_content: str) -> Any:
        return float(arg_content)


class FloatArrayDO(IDeclarativeOption):
    def get_value(self) -> Optional[List[float]]:
        o = super().get_value()
        if o is None:
            return None
        return [float(e) for e in o]

    def handle_input(self, arg_content: str) -> Any:
        return float(arg_content)
