from typing import Optional, Any, Union, List, Dict, Tuple, Callable

from ..node import DrbNode
from ..mutable_node import MutableNode
from ..path import Path, parse_path, ParsedPath
from ..exceptions import DrbException
from pathlib import PurePath


class DrbLogicalNode(MutableNode):
    """Logical Node for Drb
    This node implements an in-memory logical node, It can be used as default
    node for virtual nodes hierarchy. It can also be used as a wrapper of
    the source node, in this case, the source node is clone.

    Parameters:
        source (DrbNode | str | Path | PurePath):
    Keyword Arguments:
        namespace_uri (str): namespace URI of node - Used only if source is not
                             a DrbNode
        parent (DrbNode): parent of node - Used only if source is not a DrbNode
        value (Any): value of node - Used only if source is not a DrbNode
    """
    def __init__(self, source: Union[str, Path, PurePath], **kwargs):
        super(DrbLogicalNode, self).__init__()
        self._path_source = parse_path(source)
        self._name = self._path_source.filename
        self._namespace_uri = kwargs.get('namespace_uri', None)
        self._value = kwargs.get('value', None)
        self._parent = kwargs.get('parent', None)
        self._attributes = {}
        self._children = []

    @property
    def path(self) -> ParsedPath:
        if self._path_source.absolute or super().parent is None:
            path = self._path_source
        else:
            path = super().parent.path / self._path_source
        return path

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: Dict[Tuple[str, str], Any]) -> None:
        keys = set(self.attributes.keys())
        for n, ns in keys:
            self.remove_attribute(n, ns)
        for n, ns in attributes:
            self.add_attribute(n, attributes[n, ns], ns)

    @property
    def children(self) -> List[DrbNode]:
        return self._children

    @children.setter
    def children(self, children: List[MutableNode]) -> None:
        for idx in range(len(self)):
            self.remove_child(idx)
        for child in children:
            self.append_child(child)

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(
            f"Implementation for {impl.__name__} not supported.")

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        try:
            return self._attributes[(name, namespace_uri)]
        except (IndexError, TypeError, KeyError) as error:
            raise DrbException(f'No attribute {name} found') from error

    def close(self) -> None:
        pass

    def __str__(self):
        string = '<'
        if self.namespace_uri:
            string = string + f"{self.namespace_uri}:"
        string = string + f"{self.name}"
        if self.attributes:
            for name, namespace in self.attributes.keys():
                string = string + ' "'
                if namespace:
                    string = string + f'{namespace}:'
                string = string + f'{name}"="'
                string = \
                    string + f'{str(self.attributes.get((name, namespace)))}"'
        if self.value:
            string = string + f'>{str(self.value)}</{self.name}>'
        else:
            string = string + '/>'
        return string

    def __repr__(self):
        return self.__str__()

    def _insert_child(self, index: int, node: MutableNode) -> None:
        self._children.insert(index, node)

    def _append_child(self, node: MutableNode) -> None:
        self._children.append(node)

    def _replace_child(self, index: int, new_node: MutableNode) -> None:
        self._children[index] = new_node

    def _remove_child(self, index: int) -> None:
        del self._children[index]

    def _add_attribute(self, name: str, value: Optional[Any] = None,
                       namespace_uri: Optional[str] = None) -> None:
        if (name, namespace_uri) in self._attributes:
            raise DrbException(f'Attribute ({name}, {namespace_uri})'
                               f'already exist')
        self._attributes[name, namespace_uri] = value

    def _update_attribute_value(self, name: str, value: Any,
                                namespace_uri: str = None) -> None:
        if (name, namespace_uri) not in self._attributes:
            raise DrbException('Attribute not found: ('
                               f'{name}, {namespace_uri})')
        self._attributes[name, namespace_uri] = value

    def _remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        if (name, namespace_uri) in self._attributes:
            del self._attributes[name, namespace_uri]


class WrappedNode(MutableNode):
    def __init__(self, node: DrbNode):
        super().__init__()
        self._wrapped = node

    def __check_mutability(self):
        if not isinstance(self._wrapped, MutableNode):
            raise DrbException('Current wrapped node is not mutable')

    @property
    def name(self) -> str:
        return self._wrapped.name

    @name.setter
    def name(self, new_name):
        self.__check_mutability()
        self._wrapped.name = new_name

    @property
    def namespace_uri(self) -> str:
        return self._wrapped.namespace_uri

    @namespace_uri.setter
    def namespace_uri(self, new_namespace):
        self.__check_mutability()
        self._wrapped.namespace_uri = new_namespace

    @property
    def value(self) -> Optional[Any]:
        return self._wrapped.value

    @value.setter
    def value(self, new_value):
        self.__check_mutability()
        self._wrapped.value = new_value

    @property
    def parent(self) -> str:
        return self._wrapped.parent

    @parent.setter
    def parent(self, new_parent):
        self.__check_mutability()
        self._wrapped.parent = new_parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._wrapped.attributes

    @attributes.setter
    def attributes(self, new_attributes: Dict[Tuple[str, str], Any]) -> None:
        self.__check_mutability()
        self._wrapped.attributes = new_attributes

    @property
    def children(self) -> List[DrbNode]:
        return self._wrapped.children

    @children.setter
    def children(self, new_children: List[DrbNode]):
        self.__check_mutability()
        self._wrapped.children = new_children

    def _insert_child(self, index: int, node: DrbNode) -> None:
        self.__check_mutability()
        self._wrapped.insert_child(index, node)

    def _append_child(self, node: DrbNode) -> None:
        self.__check_mutability()
        self._wrapped.append_child(node)

    def _replace_child(self, index: int, new_node: DrbNode) -> None:
        self.__check_mutability()
        self._wrapped.replace_child(index, new_node)

    def _remove_child(self, index: int) -> None:
        self.__check_mutability()
        self._wrapped.remove_child(index)

    def _add_attribute(self, name: str, value: Optional[Any] = None,
                       namespace_uri: Optional[str] = None) -> None:
        self.__check_mutability()
        self._wrapped.add_attribute(name, value, namespace_uri)

    def _update_attribute_value(self, name: str, value: Any,
                                namespace_uri: str = None) -> None:
        self.__check_mutability()
        self._wrapped.update_attribute_value(name, value, namespace_uri)

    def _remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        self.__check_mutability()
        self._wrapped.remove_attribute(name, namespace_uri)

    def has_impl(self, impl: type) -> bool:
        return self._wrapped.has_impl(impl)

    def get_impl(self, impl: type, **kwargs) -> Any:
        return self._wrapped.get_impl(impl, kwargs)

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        return self._wrapped.get_attribute(name, namespace_uri)

    def close(self) -> None:
        self._wrapped.close()

    def register(self, event_type: str, callback: Callable):
        self.__check_mutability()
        self._wrapped.register(event_type, callback)

    def unregister(self, event_type: str, callback: Callable):
        self.__check_mutability()
        self._wrapped.unregister(event_type, callback)
