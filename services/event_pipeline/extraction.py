from abc import ABC,abstractmethod
from packages.contracts.event import Event
class EventExtractor(ABC):
 @property
 @abstractmethod
 def version(self)->str: ...
 @abstractmethod
 def extract(self,observation_ids:tuple[str,...])->list[Event]: ...
