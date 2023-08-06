from typing import Callable, Type

from .cats import Category
from .core import analyze

__all__ = "Param", "ARGV", "meta"


class Param:
    def __init__(
        self,
        name: str,
        desc: str,
        *,
        regex: str | list[str] | None = None,
        holder: str | list[str] | None = None,
    ) -> None:
        if isinstance(holder, str):
            holder = [holder]
        if isinstance(regex, str):
            regex = [regex]

        self.name = name
        self.desc = desc
        self.regex = regex
        self.placeholder = holder


ARGV = Param("argv", "Command line arguments ### 命令行参数")


def remap_cats(cats):
    from collections import defaultdict
    ret = defaultdict(list)
    for cat in cats:
        assert isinstance(cat, Category)
        ret[cat.__class__].append(cat)
    return ret


def meta(exports: list | None = None,
         *,
         desc: str | None = None,
         params: Param | list[Param] | None = None,
         cats: Category | list[Category]
         | dict[Type[Category], list[Category]]
         | None = None,
         tags: list[str] | None = None,
         ext: dict | None = None) -> Callable:
    if isinstance(params, Param):
        params = [params]
    if isinstance(cats, Category):
        cats = [cats]
    if isinstance(cats, list):
        cats = remap_cats(cats)
    data = {k: v for k, v in locals().items() if v is not None}
    if exports:
        return data  # type: ignore

    return lambda func: analyze(func, data)
