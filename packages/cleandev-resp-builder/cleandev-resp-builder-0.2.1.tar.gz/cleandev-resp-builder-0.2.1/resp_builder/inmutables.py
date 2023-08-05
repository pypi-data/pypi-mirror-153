from backports.strenum import StrEnum

class _Groups(StrEnum):
    RESP_BUILDER = 'RESP_BUILDER'

class _Properties(StrEnum):
    NAME_FILE_CODES = 'name_file_codes'


class _DictKey(StrEnum):
    DATA = 'data'
    IS_MERGE = 'is_merge'
    MIMETYPE = 'mimetype'
    EXTRADATA = 'extradata'
    STATUS_CODE = 'statud_code'
