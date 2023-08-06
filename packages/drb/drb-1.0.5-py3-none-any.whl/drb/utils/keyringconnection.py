import keyring
import logging
from keyring.errors import KeyringError
from keyrings.cryptfile.cryptfile import CryptFileKeyring
from requests.auth import AuthBase, HTTPBasicAuth

"""
This code uses keyring library to safety store username and password for
any services in the configured keyring. The current code implements
single command line able to add/remove/check entries from the keyring.

On linux ubuntu, the default keyring is gnome app name `seahorse`, but kwallet
is also
   pros:
     - unique and secure password storage solution
     - single interface to store credential
     - multiple backends and alternatives are possible (see doc
        at https://keyring.readthedocs.io/en/latest).
   cons:
     - library API exposes only basic authentication username/password.
       Usage of OAuth2.0/Certificates/ssh key requires some alternatives.
     - The keyring used in backend (ubuntu) is the gnome GUI that requires
       advanced configuration to be used without gui (see Linux headless notes
       here after)

The analysis only identified this library to store passwords.


Linux headless notes
--------------------
When Linux system is run without GUI, the keyring can still be used with dbus.

```shell
dbus-run-session -- sh
echo 'somecredstorepass' | gnome-keyring-daemon --unlock
```
(Source: https://keyring.readthedocs.io/en/latest/
    #using-keyring-on-headless-linux-systems)

Notes of 02/05/2022:
As far as keyring manage service credentail storage by (service, username)
primary key pair, it is not possible to retrieve username for a service.
The alternative consists in store services information by key has a hash map:
{service=service_name, username=key_name, password=key_info}
where key_name is a fixed string (i.e. 'username', 'password' ...)
  and key value is the value.

This change resolved the limitation of storing OAuth2.0 settings, because the
key/value information stored for one service is not limited.
A dedicated mechanism shall be defined to manage multiple credentials
per service. But this use case is currently not handled by the rest of the
system.

The bad border effect is the external tools are not any more able to
add/remove new service credential for this library.
"""
logger = logging.getLogger('drb-keyring')
init = False
_verbose = False


def _log_kr_info(verbose: bool) -> None:
    """
    printout keyring backend in logs when according to verbose parameter.

    Parameters:
        verbose (bool): displays the message when true.
    """
    if not verbose:
        return
    try:
        kr = keyring.get_keyring()
        logger.info(f'Using keyring backend {type(kr)}.')
    except Exception:
        logger.info(f'Keyring not properly set.')


def _init_keyring_backed() -> None:
    """
    The keyring backend shall be initialized according to the installed
    implementation. On Linux ubuntu, default gnome keyring is active and no
    additional feature is required.
    When no keyring is installed/accessible by default, this initialization
    creates an encrypted local file to store password.
    Thanks to his facility the mechanism never fails, but the latter is
    slightly less safe than system managed keyring.
    """
    global init, _verbose
    if init:
        _log_kr_info(_verbose)
        return
    try:
        keyring.get_keyring()
    except Exception:
        kr = CryptFileKeyring()
        kr.keyring_key = 'a25Za/.?$'  # Warn: Same as PlaintextKeyring
        keyring.set_keyring(kr)
    _log_kr_info(_verbose)
    init = True


def set_verbose(verbose: bool):
    """
    Used to make the keyring functions noisy.

    Parameters:
        verbose (bool): set verbose when true.
    """
    global _verbose
    _verbose = verbose


def kr_add_internal(service: str, key: str, value: str) -> None:
    """
    Add a nye key/value into the keyring. The keyring is managed by the
    triplet (service, username, password), in many case it is requires to
    store more than these tree keys (OAUth2.0 case). An other problem to the
    keyring system was raised when trying to retrieve credential without the
    username: system avoid this case and does not returns credential with
    service name only.
    To encounter this issue the username field is used as a key field,
    and the password field is used as value field. Then to store username and
    password, 2 entries are created into the keyring.

    Parameters:
        service (str): the service name.
        key (str): the static key name to store in keyring username.
        value (str): the value to store in password.
    """
    global _verbose
    _init_keyring_backed()
    if _verbose:
        logger.info(f"Add into keyring {service}/{key}.")
    keyring.set_password(service_name=service,
                         username=key,
                         password=value)


def kr_get_internal(service: str, key: str) -> str:
    """
    Retrieves the value related to the passed key.

    Parameters:
        service (str): the service name.
        key (str): the static key to retrieve the value
    Returns:
        str: the related value related to the key
    Raises:
        KeyringError: if no value found
    """
    _init_keyring_backed()
    credential = keyring.get_credential(service, key)
    if credential:
        return credential.password
    else:
        raise KeyringError(f"Service {service}/{key} not found.")


def kr_check_internal(service: str, key: str) -> bool:
    """
    Checks is a key exists for the service is a keyring.

    Parameters:
        service (str): the service name.
        key (str): the key to retrieve the value
    Returns:
        bool: True is a service/key/value is present in the keyring,
              False otherwise.
    """
    global _verbose
    _init_keyring_backed()
    credential = keyring.get_credential(service, key)
    if credential:
        if _verbose:
            logger.info(f"Found {service}/{key}.")
        return True
    else:
        if _verbose:
            logger.info(f"Service {service}/{key} not found.")
        return False


def kr_remove_internal(service: str, key:  str) -> None:
    """
    Removes a (service, key, value) triplet from the keyring.

    Parameters:
        service (str): the service name.
        key (str): the key to retrieve the value.
    Raises:
        PasswordDeleteError: when entry cannot be removed.
    """
    global _verbose
    _init_keyring_backed()
    if _verbose:
        logger.info(f"Remove from keyring {service}/{key}.")
    keyring.delete_password(service, key)


def kr_add(service: str, username: str, password: str):
    """
    Add service credentials into the keyring.
    The internal functions are used here to separately store username and
    password into respective triplets: (service, 'username', username) and
    (service, 'password', password)
    """
    kr_add_internal(service=service, key='username', value=username)
    kr_add_internal(service=service, key='password', value=password)


def kr_remove(service: str):
    """
    Remove service credentials from the keyring.
    The internal functions are used to manage these action.

    Parameters:
        service (str): service name or URI

   .. seealso:: kr_add and kr_add_internal to details the credential
                keyring handling.
    """
    kr_remove_internal(service=service, key='username')
    kr_remove_internal(service=service, key='password')


def kr_get(service: str, username: str = None) -> dict:
    """
    Retrieves credentials for a service. When username is not provided, system
    retrieves it if the service exists in the keyring.

    Parameters:
        service (str): the service url.
        username (str): the username (can be None)
    Returns:
        dict: containing names credentials such as 'username' and 'password'.
    Raises:
        KeyringError: when service or user not found.
    """
    _username = kr_get_internal(service=service, key='username')
    if username is not None and _username != username:
        raise KeyringError(f"Username not found ({username})")

    password = kr_get_internal(service=service, key='password')
    return {'username': _username, 'password': password}


def kr_check(service: str, username: str = None) -> bool:
    """
    Checks is the service exists in keyring.

    Parameters:
        service (str): the service url.
        username (str): the username (can be None)
    Returns:
        bool: True when service exists. Is username is provided, return true
              if the service exists for the passed username, false otherwise.
    """
    _username = None
    if username is not None:
        try:
            _username = kr_get_internal(service=service, key='username')
        except Exception:
            # case of no username found for the service
            return False
    if _username is not None and _username != username:
        return False
    try:
        password = kr_get_internal(service=service, key='password')
    except Exception:
        # Case of passed username is None and service not found.
        return False
    if password is not None:
        return True


def kr_get_auth(service: str, username: str = None) -> AuthBase:
    """
    Build the authentication structure compatible with request API to
    allow connections wrt to the information stored into the keyring.

    The keyring hardcoded dict keys to identify username/password and the
    credential information. To limit the usage of these internal keys outside
    this package, this function build AuthBase structure from data retrieved
    from keyring.

    Parameters:
        service (str): the service url.
        username (str): the username (can be None)
    Returns:
        auth: the authentication structure to connect remote service.
    Raises:
        KeyringError: when service or user not found in keyring.
    """
    credential = kr_get(service, username)
    # Recovers all elements of known kinds of credentials
    username = credential.get('username')
    password = credential.get('password')
    auth_url = credential.get('auth_url')
    tenant_id = credential.get('tenant_id')
    tenant_name = credential.get('tenant_name')
    project_id = credential.get('project_id')
    project_name = credential.get('project_name')
    user_domain_name = credential.get('user_domain_name')
    region_name = credential.get('region_name')
    auth_version = credential.get('auth_version')

    # Case of no external auth service
    if auth_url is None:
        return HTTPBasicAuth(username=username, password=password)

    # This implementation only manage basic auth.
    raise NotImplementedError("Authentication not implemented.")
