import abc
from uuid import UUID

from src.rock.domain.entities import DetectionCreate, DetectionUpdate
from src.rock.domain.entities import Detection


class IDetectionRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_pk(self, pk: UUID) -> Detection: ...

    @abc.abstractmethod
    async def create(self, detection_data: DetectionCreate) -> Detection: ...

    @abc.abstractmethod
    async def update_by_pk(self, pk: UUID, detection_data: DetectionUpdate) -> Detection: ...
