from __future__ import annotations

import argparse
from typing import Dict, List, Optional, Sequence, Type, cast

from declarative_argparse.options.abc import IDeclarativeOption
from declarative_argparse.options.bool import BoolArrayDO, BoolDO
from declarative_argparse.options.float import FloatArrayDO, FloatDO
from declarative_argparse.options.int import IntArrayDO, IntDO
from declarative_argparse.options.str import StrArrayDO, StrDO

__version__ = '0.0.1'
__all__ = [
    'BoolArrayDO',
    'BoolDO',
    'DeclarativeOptionParser',
    'FloatArrayDO',
    'FloatDO',
    'IntArrayDO',
    'IntDO',
    'StrArrayDO',
    'StrDO',
]


class DeclarativeOptionParser:
    def __init__(self, argp: Optional[argparse.ArgumentParser]) -> None:
        self.argp = argp or argparse.ArgumentParser()
        self.allOpts: List[IDeclarativeOption] = []
        self.allOptsByID: Dict[str, IDeclarativeOption] = {}

        #self.verbose: BoolDO = self.addBool('quiet', 'q', 'Removes verbosity of output')
    def bindToNamespace(self, args: argparse.Namespace) -> None:
        [x._bindToNamespace(args) for x in self.allOpts]

    def parseArguments(self, args: Optional[Sequence[str]]=None) -> None:
        for arg in self.allOpts:
            arg.add_to_argparser(self.argp)
        self.bindToNamespace(self.argp.parse_args(args))

    def add(self,
            t: Type[IDeclarativeOption],
            longform: str,
            shortform: Optional[str] = None,
            description: Optional[str] = None) -> IDeclarativeOption:
        do = t(self, longform, shortform, description)
        self.allOpts.append(do)
        self.allOptsByID[do.id] = do
        return do

    def addBool(self,
                longform: str,
                shortform: Optional[str] = None,
                description: Optional[str] = None) -> BoolDO:
        return cast(BoolDO, self.add(BoolDO, longform, shortform, description))

    def addBoolArray(self,
                     longform: str,
                     nargs: str,
                     shortform: Optional[str] = None,
                     description: Optional[str] = None) -> BoolArrayDO:
        return cast(BoolArrayDO, self.add(BoolArrayDO, longform, shortform, description)).setNArgs(nargs)

    def addFloat(self,
                 longform: str,
                 shortform: Optional[str] = None,
                 description: Optional[str] = None) -> FloatDO:
        return cast(FloatDO, self.add(FloatDO, longform, shortform, description))

    def addFloatArray(self,
                      longform: str,
                      nargs: str,
                      shortform: Optional[str] = None,
                      description: Optional[str] = None) -> FloatArrayDO:
        return cast(FloatArrayDO, self.add(FloatArrayDO, longform, shortform, description)).setNArgs(nargs)

    def addInt(self,
               longform: str,
               shortform: Optional[str] = None,
               description: Optional[str] = None) -> IntDO:
        return cast(IntDO, self.add(IntDO, longform, shortform, description))

    def addIntArray(self,
                    longform: str,
                    nargs: str,
                    shortform: Optional[str] = None,
                    description: Optional[str] = None) -> IntArrayDO:
        return cast(IntArrayDO, self.add(IntArrayDO, longform, shortform, description)).setNArgs(nargs)

    def addStr(self,
               longform: str,
               shortform: Optional[str] = None,
               description: Optional[str] = None) -> StrDO:
        return cast(StrDO, self.add(StrDO, longform, shortform, description))

    def addStrArray(self,
                    longform: str,
                    nargs: str,
                    shortform: Optional[str] = None,
                    description: Optional[str] = None) -> StrArrayDO:
        return cast(StrArrayDO, self.add(StrArrayDO, longform, shortform, description)).setNArgs(nargs)
