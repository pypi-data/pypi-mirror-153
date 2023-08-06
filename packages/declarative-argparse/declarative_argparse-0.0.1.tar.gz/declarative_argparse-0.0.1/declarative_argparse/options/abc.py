from __future__ import annotations

import argparse
import typing
from abc import ABC, abstractmethod
from typing import Any, Collection, Dict, List, Optional

if typing.TYPE_CHECKING:
    from declarative_argparse import DeclarativeOptionParser


class IDeclarativeOption(ABC):
    def __init__(self,
                 dop: 'DeclarativeOptionParser',
                 longform: str,
                 shortform: Optional[str] = None,
                 description: Optional[str] = None) -> None:
        self.dop: 'DeclarativeOptionParser' = dop
        self.id: str = longform.replace('-', '_').strip('_')
        self.longform: str = longform
        self.shortform: Optional[str] = shortform
        self.description: Optional[str] = description
        self.nargs: Optional[str] = None
        self.const: Optional[Any] = None
        self.default: Any = None
        self.choices: Optional[Collection[str]] = None
        self.required: Optional[bool] = None
        self.metavar: Optional[str] = None
        self.version: Optional[str] = None

        self.action: Optional[argparse.Action] = None
        self._args: Optional[argparse.Namespace] = None

    def _bindToNamespace(self, args: argparse.Namespace) -> None:
        self._args = args

    def setNArgs(self, nargs: Optional[str]) -> IDeclarativeOption:
        self.nargs = nargs
        return self

    def setLongForm(self, val: str) -> IDeclarativeOption:
        self.longform = val
        return self

    def setShortForm(self, val: Optional[str]) -> IDeclarativeOption:
        self.shortform = val
        return self

    def setDescription(self, val: Optional[str]) -> IDeclarativeOption:
        self.description = val
        return self

    def setConst(self, val: Optional[Any]) -> IDeclarativeOption:
        self.const = val
        return self

    def setDefault(self, val: Any) -> IDeclarativeOption:
        self.default = val
        return self

    def setRequired(self, val: Optional[bool]) -> IDeclarativeOption:
        self.required = val
        return self

    def setMetaVar(self, val: Optional[bool]) -> IDeclarativeOption:
        self.metavar = val
        return self

    def setVersion(self, val: Optional[bool]) -> IDeclarativeOption:
        self.version = val
        return self

    def add_to_argparser(self, argp: argparse.ArgumentParser) -> None:
        args: List[str] = [self.longform]
        if self.shortform is not None:
            args.append(self.shortform)
        kwargs: Dict[str, Any] = {}
        kwargs['type'] = self.handle_input
        if self.description is not None:
            kwargs['help'] = self.description
        if self.nargs is not None:
            kwargs['nargs'] = self.nargs
        if self.const is not None:
            kwargs['nargs'] = self.const
        kwargs['default'] = self.default
        if self.choices is not None:
            kwargs['choices'] = self.choices
        if self.required is not None:
            kwargs['required'] = self.required
        if self.metavar is not None:
            kwargs['metavar'] = self.metavar
        if self.version is not None:
            kwargs['version'] = self.version
        self.action = argp.add_argument(*args, **kwargs)

    def get_value(self) -> Optional[Any]:
        return getattr(self._args, self.id, None)

    @abstractmethod
    def handle_input(self, arg_content: str) -> Any:
        pass
