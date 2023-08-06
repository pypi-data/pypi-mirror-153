from ._version import get_versions
from .item import DrbItem
from .node import DrbNode
from .abstract_node import AbstractNode
from .mutable_node import MutableNode
from .factory.factory_resolver import resolve_children

__version__ = get_versions()['version']
del get_versions
__all__ = [
    'DrbItem',
    'DrbNode',
    'AbstractNode',
    'MutableNode',
    'resolve_children',
]
