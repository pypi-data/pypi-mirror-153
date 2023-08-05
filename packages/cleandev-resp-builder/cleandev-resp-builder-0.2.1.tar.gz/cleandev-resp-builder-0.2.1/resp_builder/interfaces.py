from abc import ABC
from abc import abstractmethod

class ResponseBuilderInterface(ABC):

    @abstractmethod
    def response(
        self,
        code: str = '',
        data: dict = None,
        status_code: int = 500,
        is_merge: bool = False
    ) -> dict:
        raise NotImplemented


