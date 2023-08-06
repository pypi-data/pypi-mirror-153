
from abc import ABC, abstractmethod
from typing import Dict, List, TypeVar, Generic

T = TypeVar('T')

class IAtomicUserInteraction(ABC):

    @abstractmethod
    def notify_user(self, text: str):
        pass

    @abstractmethod
    def request_string(self, prompt: str):
        pass

    @abstractmethod
    def request_int(self, prompt: str):
        pass

    @abstractmethod
    def request_enum(self, enum, prompt:str=None):
        pass

    @abstractmethod
    def request_float(self, prompt: str):
        pass

    @abstractmethod
    def request_guid(self, prompt: str):
        pass

    @abstractmethod
    def request_date(self, prompt: str = None):
        pass

    @abstractmethod
    def request_from_dict(self, selectionDict: Dict[int, str], prompt=None) -> int:
        pass

    @abstractmethod
    def request_from_list(self, selectionList: List[str], prompt=None) -> str:
        pass

    @abstractmethod
    def request_from_objects(self, selectionList: List[T], objectIdentifier: str, prompt=None) -> T:
        pass

    @abstractmethod
    def request_open_filepath(self):
        pass

    @abstractmethod
    def request_save_filepath(self):
        pass

    @abstractmethod
    def request_you_sure(self, prompt=None):
        pass

    @abstractmethod
    def request_bool(self, prompt=None):
        pass



