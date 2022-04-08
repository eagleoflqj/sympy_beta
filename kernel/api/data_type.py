# todo: merge _Class and Class when https://github.com/python/mypy/issues/6131 is resolved
from __future__ import annotations

from typing import Sequence, TypedDict

from typing_extensions import NotRequired


class Dict(TypedDict):
    type: str


class _Tex(Dict):
    tex: str
    numeric: NotRequired[bool]
    expression: NotRequired[str]
    approximation: NotRequired[str]


def Tex(tex: str):
    return _Tex(type='Tex', tex=tex)


class _ChineseNumeral(Dict):
    normal: str
    financial: str


def ChineseNumeral(normal: str, financial: str):
    return _ChineseNumeral(type='ChineseNumeral', normal=normal, financial=financial)


class _Document(Dict):
    html: str


def Document(html: str):
    return _Document(type='Document', html=html)


class _Reference(Dict):
    links: list[str]


def Reference(links: list[str]):
    return _Reference(type='Reference', links=links)


class _Table(Dict):
    titles: Sequence[str]
    rows: list[list[str]]


def Table(titles: Sequence[str], rows: list[list[str]]):
    return _Table(type='Table', titles=titles, rows=rows)


def TruthTable(titles: Sequence[str], rows: list[list[str]]):
    return _Table(type='TruthTable', titles=titles, rows=rows)


class _List(Dict):
    list: list[Dict]


def List(list: list[Dict]):
    return _List(type='List', list=list)


class _FactorDiagram(Dict):
    primes: list[int]


def FactorDiagram(primes: list[int]):
    return _FactorDiagram(type='FactorDiagram', primes=primes)


class _Plot(Dict):
    variable: str
    graphs: list[dict]


def Plot(variable: str, graphs: list[dict]):
    return _Plot(type='Plot', variable=variable, graphs=graphs)


class _Text(Dict):
    text: str


def Text(text: str):
    return _Text(type='Text', text=text)


class _Svg(Dict):
    svg: str
    name: str


def Svg(svg: str, name: str):
    return _Svg(type='Svg', svg=svg, name=name)


class _ContinuedFraction(Dict):
    n: int
    finite: list[int]
    repeated: list[int] | None


def ContinuedFraction(n: int, finite: list[int], repeated: list[int] | None):
    return _ContinuedFraction(type='ContinuedFraction', n=n, finite=finite, repeated=repeated)
