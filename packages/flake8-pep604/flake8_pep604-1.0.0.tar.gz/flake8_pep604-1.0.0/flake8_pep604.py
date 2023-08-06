from __future__ import annotations

import ast
import sys

if sys.version_info >= (3, 8):  # pragma: >=3.8 cover
    import importlib.metadata as importlib_metadata
else:  # pragma: <3.8 cover
    import importlib_metadata

from typing import Any, Generator

MSG = "UNT001 use `|` in place of `typing.Union`. See PEP-604"


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        visitor = _Visitor()
        visitor.visit(self._tree)

        for line, col in visitor.union_imports:
            yield line, col, MSG, type(self)


class _Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.union_imports: list[tuple[int, int]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            if name.name == "typing.Union":
                self.union_imports.append((node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "typing":
            for name in node.names:
                if name.name == "Union":
                    self.union_imports.append((node.lineno, node.col_offset))
        self.generic_visit(node)
