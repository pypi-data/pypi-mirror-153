from typing import Any, List, Optional

from declarative_argparse.options.abc import IDeclarativeOption


class BoolDO(IDeclarativeOption):
    def get_value(self) -> Optional[bool]:
        o = super().get_value()
        if o is None:
            return None
        return bool(o)

    def handle_input(self, arg_content: str) -> Any:
        return bool(arg_content)


class BoolArrayDO(IDeclarativeOption):
    def get_value(self) -> Optional[List[bool]]:
        o = super().get_value()
        if o is None:
            return None
        return [bool(e) for e in o]

    def handle_input(self, arg_content: str) -> Any:
        return bool(arg_content)
