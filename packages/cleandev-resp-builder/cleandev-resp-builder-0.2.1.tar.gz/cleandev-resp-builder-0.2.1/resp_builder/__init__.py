import json
from flask import Response
from resp_builder.inmutables import _DictKey
from resp_builder.config import _name_file_codes
from resp_builder.config import _default_mimetype
from resp_builder.config import _default_response
from resp_builder.config import _default_response
from resp_builder.config import _name_file_codes
from resp_builder.config import _default_status_code
from resp_builder.interfaces import ResponseBuilderInterface as Rbi


class ResponseBuilder(Rbi):

    def __init__(self):
        file = open(_name_file_codes)
        self.__codes = json.load(file)

    def __get_data_from_code(self, code: str):
        if not code or not dict(self.__codes).get(code):
            return _default_response
        return dict(self.__codes).get(code)

    def response(
        self,
        code: str = '',
        data: dict = None,
        status_code: int = 500,
        is_merge: bool = False
    ) -> dict:

        if code and not data:
            tmp: dict = self.__get_data_from_code(code)
            return Response(json.dumps(tmp), status=status_code, mimetype=_default_mimetype)

        if code and data and not is_merge:
            tmp: dict = self.__get_data_from_code(code)
            tmp = tmp | {'data': data}
            return Response(json.dumps(tmp), status=status_code, mimetype=_default_mimetype)

        if code and data and is_merge:
            tmp: dict = self.__get_data_from_code(code)
            tmp = tmp | data
            return Response(json.dumps(tmp), status=status_code, mimetype=_default_mimetype)

        if not code and data:
            return Response(json.dumps(data), status=status_code, mimetype=_default_mimetype)

        return Response(json.dumps(_default_response), status=status_code, mimetype=_default_mimetype)