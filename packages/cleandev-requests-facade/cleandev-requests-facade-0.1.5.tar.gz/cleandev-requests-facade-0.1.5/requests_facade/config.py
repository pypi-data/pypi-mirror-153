import os
from properties_loader import PropertiesImpl
from properties_loader.interfaces import Properties
from generic_utils import CleanDevGenericUtils

utils: CleanDevGenericUtils = CleanDevGenericUtils()

_properties: Properties = PropertiesImpl().__dict__
_properties_endpoint_config = _properties['ENDPOINT_CONFIG']
_properties_auth: dict = _properties['AUTH']

FERNET_KEY = os.getenv('FERNET_KEY')

_auth_payload: dict = {
    _properties_auth['user_key']: utils.decrypt(_properties_auth['user_value'], FERNET_KEY),
    _properties_auth['password_key']: utils.decrypt(_properties_auth['password_value'], FERNET_KEY)
}

_endpoint_auth: str = _properties_endpoint_config['endpoint_auth']

