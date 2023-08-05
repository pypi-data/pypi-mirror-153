from properties_loader.interfaces import Properties
from properties_loader import PropertiesImpl
from resp_builder.inmutables import _Groups
from resp_builder.inmutables import _Properties

_properties: Properties = PropertiesImpl().__dict__

RESP_BUILDER: str = str(_Groups.RESP_BUILDER)
NAME_FILE_CODES: str = str(_Properties.NAME_FILE_CODES)

_name_file_codes = _properties[RESP_BUILDER][NAME_FILE_CODES]
_default_response: dict = {'message': "Error"}
_default_mimetype: str = 'application/json'
_default_status_code: int = 500

