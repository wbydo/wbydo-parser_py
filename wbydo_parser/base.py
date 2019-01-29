from typing import TypeVar, Generic
from typing_extensions import Protocol

from dataclasses import dataclass

V = TypeVar('V')
N = TypeVar('N')


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Result(Generic[V, N]):
    value: V
    next: N


@dataclass(init=True, repr=True, eq=True, frozen=True)
class ParseError(Exception, Generic[N]):
    next: N
    msg: str = 'ParseError'


class ParserFunction(Protocol[V, N]):
    def __call__(self, input: N) -> Result[V, N]:
        raise NotImplementedError()


class Parser(ParserFunction[V, N]):
    def __call__(self, input: N) -> Result[V, N]:
        raise NotImplementedError()


SV = TypeVar('SV')
SN = TypeVar('SN')


class RequireSubParser(Parser[V, N], Generic[V, N, SV, SN]):
    subparser: Parser[SV, SN]

    def __init__(self, subparser: Parser[SV, SN]):
        super().__init__()
        self.subparser = subparser
