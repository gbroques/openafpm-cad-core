import ast
import inspect
from collections import OrderedDict
from typing import TypedDict

__all__ = ['get_docstring_by_key']


class TypedDictKeyDocstringVistor(ast.NodeVisitor):

    def __init__(self):
        self.docstring_by_key = OrderedDict()

    def visit_AnnAssign(self, node):
        key = node.target.id
        self.docstring_by_key[key] = None

    def visit_Expr(self, node):
        if len(self.docstring_by_key.keys()) > 0:
            key, value = self.docstring_by_key.popitem()
            docstring = node.value.value
            self.docstring_by_key[key] = docstring


def get_docstring_by_key(typed_dict: TypedDict) -> OrderedDict:
    source = inspect.getsource(typed_dict)
    tree = ast.parse(source)
    docstring_vistor = TypedDictKeyDocstringVistor()
    docstring_vistor.visit(tree)
    return docstring_vistor.docstring_by_key
