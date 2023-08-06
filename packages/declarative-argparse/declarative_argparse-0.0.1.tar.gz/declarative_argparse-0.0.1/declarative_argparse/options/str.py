from typing import Any, List, Optional

from declarative_argparse.options.abc import IDeclarativeOption


class StrDO(IDeclarativeOption):
    def get_value(self) -> Optional[str]:
        o = super().get_value()
        if o is None:
            return None
        return str(o)

    def handle_input(self, arg_content: str) -> Any:
        return str(arg_content)


class StrArrayDO(IDeclarativeOption):
    def get_value(self) -> Optional[List[str]]:
        o = super().get_value()
        if o is None:
            return None
        return [str(e) for e in o]

    def handle_input(self, arg_content: str) -> Any:
        return str(arg_content)
