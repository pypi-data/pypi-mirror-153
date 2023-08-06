import io
import requests
from urllib.request import urlopen
from requests.auth import AuthBase
from typing import Any, Optional, List, Dict, Tuple, Union

from ..node import DrbNode
from ..path import ParsedPath, Path, parse_path
from ..exceptions import DrbException
from .keyringconnection import kr_check, kr_get_auth


class UrlNode(DrbNode):
    """
    URL node is a simple implementation of DrbNode base on a given URL without
    any attribute or child. This node must be use only in this core library
    (drb) and not in any implementation. It's mainly uses to generate the root
    node generated from an URI.
    """
    def __init__(self, source: Union[str, Path, ParsedPath],
                 auth: AuthBase = None):
        """
        The construction of an UrlNode.

        Parameters:
            source (str, Path, ParsedPAth): the url to the service
            auth (AuthBase): the authentication(Optional)

        """
        super().__init__()
        self._path = parse_path(source)
        self._auth = auth

    @property
    def name(self) -> str:
        return self._path.filename

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException('UrlNode has no attribute')

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def path(self) -> ParsedPath:
        return self._path

    @property
    def children(self) -> List[DrbNode]:
        return []

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        return False

    def has_impl(self, impl: type) -> bool:
        if issubclass(io.BytesIO, impl):
            return True
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        if not self.has_impl(impl):
            raise DrbException(f'Unsupported implementation: {impl}')
        try:
            orginal_path = self._path.original_path
            if 'file' == self._path.scheme:
                path = orginal_path[7:]
                return open(path, 'rb')
            if '' == self._path.scheme:
                return open(orginal_path, 'rb')
            return requests.get(orginal_path,
                                auth=self._find_credential(orginal_path))
        except Exception as ex:
            raise DrbException(f'Unsupported URL') from ex

    def close(self) -> None:
        pass

    def __len__(self):
        return 0

    def __getitem__(self, item):
        raise DrbException('UrlNode has no child')

    def __truediv__(self, child):
        raise DrbException('UrlNode has no child')

    def _find_credential(self, url: str):
        if self._auth is not None:
            return self._auth

        if kr_check(url):
            return kr_get_auth(url)

        return None
