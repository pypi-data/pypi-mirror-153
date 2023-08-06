from __future__ import annotations
import abc
from typing import Any, Optional

from .node import DrbNode
from .path import ParsedPath
from .abstract_node import AbstractNode
from .exceptions import DrbException


class MutableNode(AbstractNode, abc.ABC):
    """
    A mutable DrbNode able to manage changes on its properties and also
    manage addition and removing of his children and attributes without
    performing any writing on the resource targeted by this node.
    """

    __event_type_names = {
        'name-changed',
        'namespace-changed',
        'value-changed',
        'child-added',
        'child-removed',
        'child-changed',
        'attribute-added',
        'attribute-removed',
        'attribute-changed',
    }

    def __init__(self, **kwargs):
        super(MutableNode, self).__init__()
        self._name = None
        self._namespace_uri = None
        self._value = None
        self._path = None
        self._parent = None
        for event_name in self.__event_type_names:
            self._event_manager.append_event_type(event_name)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        old = self.name
        if old != name:
            self._name = name
            self._event_manager.notify('name-changed', self, old, name)

    @property
    def namespace_uri(self) -> Optional[str]:
        return self._namespace_uri

    @namespace_uri.setter
    def namespace_uri(self, namespace_uri: str) -> None:
        old = self.namespace_uri
        if old != namespace_uri:
            self._namespace_uri = namespace_uri
            self._event_manager.notify('namespace-changed', self, old,
                                       namespace_uri)

    @property
    def value(self) -> Optional[Any]:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        old = self.value
        if old != value:
            self._value = value
            self._event_manager.notify('value-changed', self, old, value)

    @property
    def path(self) -> ParsedPath:
        return self._path

    @path.setter
    def path(self, path: ParsedPath) -> None:
        self._path = path

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @parent.setter
    def parent(self, parent: DrbNode) -> None:
        self._parent = parent

    @abc.abstractmethod
    def _insert_child(self, index: int, node: DrbNode) -> None:
        """
        Internal method to insert a new child to the current node.

        Parameters:
            index (int): expected index of the node after the insertion.
            node (DrbNode): node to be inserted.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _append_child(self, node: DrbNode) -> None:
        """
        Internal method to add a new child to the current node.

        Parameters:
            node (DrbNode): A reference to the node to be appended.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _replace_child(self, index: int, new_node: DrbNode) -> None:
        """
        Internal method to replace a child of the current node.

        Parameters:
            index (int): index of the replaced node
            new_node (DrbNode): the replacement node
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _remove_child(self, index: int) -> None:
        """
        Internal method to remove a child node from the current node.

        Parameters:
            index (int): Index of the child to be removed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _add_attribute(self, name: str, value: Optional[Any] = None,
                       namespace_uri: Optional[str] = None) -> None:
        """
        Internal method allowing to add an attribute to the current node.

        Parameters:
            name (str): attribute name
            value (Any): attribute name (default ``None``)
            namespace_uri (str): attribute namespace (default ``None``)
        Raises:
            DrbException: if the attribute already exists.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _update_attribute_value(self, name: str, value: Any,
                                namespace_uri: str = None) -> None:
        """
        Internal method allowing to update/change an attribute value.

        Parameters:
            name (str): attribute name
            value (Any): new attribute value
            namespace_uri (str): attribute namespace URI (default: ``None``)
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        """
        Removes the corresponding attribute.

        Parameters:
            name (str): attribute name
            namespace_uri (str): attribute namespace URI (default: `None`)

        Raises:
            DrbException: if the attribute is not found.
        """
        raise NotImplementedError

    def insert_child(self, index: int, node: MutableNode) -> None:
        """
        Inserts a child at a given position. The passed node is inserted in
        the list of children at the given position The position is the
        expected index of the node after insertion. All the previous
        children from the aimed position to the end of the list are shift to
        the end of the new children list (i.e. their indices are shifted up
        of 1). If the given index is out of the children bounds and
        therefore less than zero and greater or equal to the current number
        of children,the operation raises an exception. An index equal to the
        current number of children is allowed and the
        operation is therefore equivalent to append_child().
        If the node has been inserted within the children list, the next
        sibling indices are increased of one. In addition the associations
        between the inserted node and it previous and next siblings are
        updated (if any).

        Important note: The implementation of the node is not supposed to
        accept any kind of node For instance it may not be possible to
        insert a node wrapping a file in an XML document. The documentation
        of the implementation shall describe its specific strategy.
        Case of unordered or specifically ordered implementations:</b> If
        the implementation does not support ordered children or has specific
        ordering rules, the node is inserted without taking into account the
        requested index passed in parameter. For instance it may not be
        possible to impose the file order in a directory: it generally
        depends on the lexicographical order of the node names or their
        creation date.

        Parameters:
            index (int): expected index of the node after the insertion.
            node (MutableNode): node to be inserted.
        """
        self._insert_child(index, node)
        node.parent = self
        self._event_manager.notify('child-added', self, index, node)

    def append_child(self, node: MutableNode) -> None:
        """
        Appends a child at the end of the children list. The passed node is
        inserted in the list of children at the end of the current list.

        Note:
            The implementation of the node is not supposed to accept any kind
            of node For instance it may not be possible to append a node
            wrapping a file in an XML document. The documentation
            of the implementation shall describe its specific strategy.
            Case of unordered or specifically ordered implementations: If the
            implementation does not support ordered children or has specific
            ordering rules, the node may not be appended but only inserted
            according to these rules.

        Parameters:
            node (DrbNode): A reference to the node to be appended.
        """
        index = self.__len__()
        self._append_child(node)
        node.parent = self
        self._event_manager.notify('child-added', self, index, node)

    def replace_child(self, index: int, new_node: MutableNode) -> None:
        """
        Replaces a child of the current node. This operation replaces a
        child in the current children list by a new one The operation aborts
        when the index is out of bound (index < 0 || index > size). In case
        of error, the implementation has to restore the initial situation.
        It is therefore recommended for any implementation to check the
        consistency prior to perform the replacement.

        Important note: The implementation of the node is not supposed to
        accept any kind of node For instance it may not be possible to
        insert a node wrapping a file in an XML document. The documentation
        of the implementation shall describe its specific strategy.

        Events: This operation fires a node change event when the
        implementation is a node change producer. The node affected by the
        change is the new node and the source is the current node. The
        called operation is the structure_changed() of the listeners.

        Parameters:
            index (int): Index of the node to be replaced. This index starts at
                         0 and shall be less than the number of children.
            new_node (DrbNode): A reference to the node that replaces the old
                                one.
        """
        if len(self) < index:
            raise DrbException('Index out of range')
        old = self[index]
        if old != new_node:
            self._replace_child(index, new_node)
            new_node.parent = self
            self._event_manager.notify('child-changed', self, index, old,
                                       new_node)

    def remove_child(self, index: int) -> None:
        """
        Removes an existing child. The child at the given index is removed
        from the children list of the current node. The child is not
        modified by this operation. At the child point of view it keeps the
        same parent or any common association depending on the implementation.

        Note:
            At the parent (i.e. the current node) point
            of view the removed node is completely dismissed and will never be
            re-instantiated from constructor operations.

        Parameters
            index (int): Index of the child to be removed.
        """
        if len(self) <= index:
            raise DrbException('Index out of range')
        removed = self[index]
        self._remove_child(index)
        self._event_manager.notify('child-removed', self, index, removed)

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        """
        Adds an attribute to the current node.

        Parameters:
            name (str): attribute name
            value (Any): attribute name (default ``None``)
            namespace_uri (str): attribute namespace (default ``None``)
        Raises:
            DrbException: if the attribute already exists.
        """
        self._add_attribute(name, value, namespace_uri)
        self._event_manager.notify('attribute-added', self, name,
                                   namespace_uri, value)

    def update_attribute_value(self, name: str, value: Any,
                               namespace_uri: str = None) -> None:
        """
        Updates value of an existing attribute on the current node.

        Parameters:
            name (str): attribute name
            value (Any): new attribute value
            namespace_uri (str): attribute namespace URI (default: ``None``)
        Raises:
            DrbException: if the attribute is not found.
        """
        old = self.get_attribute(name, namespace_uri)
        if old != value:
            self._update_attribute_value(name, value, namespace_uri)
            self._event_manager.notify('attribute-changed', self, name,
                                       namespace_uri, old, value)

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        """
        Removes the corresponding attribute.

        Parameters:
            name (str): attribute name
            namespace_uri (str): attribute namespace URI (default: `None`)

        Raises:
            DrbException: if the attribute is not found.
        """
        value = self.get_attribute(name, namespace_uri)
        self._remove_attribute(name, namespace_uri)
        self._event_manager.notify('attribute-removed', self, name,
                                   namespace_uri, value)
