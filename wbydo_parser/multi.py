from typing import TypeVar, Tuple, List

from .base import RequireSubParser, Result, ParseError

V = TypeVar('V')
N = TypeVar('N')


class ZeroOrMore(RequireSubParser[Tuple[V, ...], N, V, N]):
    def __call__(self, input: N) -> Result[Tuple[V, ...], N]:
        values: List[V] = []
        next_ = input
        while True:
            try:
                result = self.subparser(next_)
            except ParseError:
                break
            else:
                values.append(result.value)
                next_ = result.next

        return Result(value=tuple(values), next=next_)


class OneOrMore(RequireSubParser[Tuple[V, ...], N, V, N]):
    def __call__(self, input: N) -> Result[Tuple[V, ...], N]:
        first_result = self.subparser(input)
        parser = ZeroOrMore(self.subparser)
        more_result = parser(first_result.next)
        return Result(
            value=(first_result.value, *more_result.value),
            next=more_result.next
        )
