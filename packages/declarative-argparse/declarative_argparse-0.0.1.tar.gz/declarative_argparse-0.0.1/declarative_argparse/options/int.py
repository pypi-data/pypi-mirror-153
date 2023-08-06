from typing import Any, List, Optional

from declarative_argparse.options.abc import IDeclarativeOption


class IntDO(IDeclarativeOption):
    def get_value(self) -> Optional[int]:
        o = super().get_value()
        if o is None:
            return None
        return int(o)

    def handle_input(self, arg_content: str) -> Any:
        return int(arg_content)


class IntArrayDO(IDeclarativeOption):
    def get_value(self) -> Optional[List[int]]:
        o = super().get_value()
        if o is None:
            return None
        return [int(e) for e in o]

    def handle_input(self, arg_content: str) -> Any:
        return int(arg_content)
