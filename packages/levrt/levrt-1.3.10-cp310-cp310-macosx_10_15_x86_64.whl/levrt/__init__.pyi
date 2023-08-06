from pathlib import Path
from typing import Any, Generator

from motor.core import AgnosticDatabase, AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient


class Digest(str):
    ...


File = bytes | str | Path | Digest


class Document:
    coll: AgnosticCollection
    filter: dict

    async def get(self, query=None, projection=None):
        ...

    async def set(self, data=None, **kwargs):
        ...

    def all(self, query=None, projection=None):
        ...


class Task:
    id: int
    host: str

    async def signal(self, signal="SIGINT"):
        ...

    async def done(self) -> Document:
        ...

    def __await__(self) -> Generator[Any, None, Document]:
        ...


class Cr:
    def __init__(
        self,
        image: str,
        schema: str | None = None,
        *,
        host=False,
        entry=None,
        cmd: list[str] = [],
        env: list[str] = [],
        files: dict[str, File] = {},
        links: dict[str, str] = {},
        ports: list[int] = [],
        services: dict[str, Cr] = {},
    ):
        ...

    async def start(self) -> Task:
        ...

    async def done(self) -> Document:
        ...

    def __await__(self) -> Generator[Any, None, Document]:
        ...


class Concurrent:
    def __init__(self, limit=None):
        ...

    def start(self, coro) -> Task:
        ...

    def __call__(self, *weights) -> int:
        ...

    async def __aenter__(self) -> Concurrent:
        ...

    async def __aexit__(self, *_):
        ...


class NamespaceContextManager:
    def __truediv__(self, sub) -> NamespaceContextManager:
        ...

    def __enter__(self) -> Document:
        ...

    def __exit__(self, *_):
        ...


class LevContext:
    proxy: str | None
    job_id: int
    mongo: AsyncIOMotorClient
    db: AgnosticDatabase
    coll: AgnosticCollection
    doc: Document

    def __truediv__(self, sub) -> NamespaceContextManager:
        ...

    def set(self, data=None, **kwargs):
        ...


def remote(func):
    ...


def cli(*args, **kwargs) -> list[str]:
    ...


def run(main, *, db=None):
    ...


ctx: LevContext
lev: LevContext
