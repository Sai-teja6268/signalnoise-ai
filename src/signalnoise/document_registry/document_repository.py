from abc import ABC, abstractmethod
from signalnoise.document_registry.document_model import DocumentMetadata


class DocumentRepository(ABC):

    @abstractmethod
    def save(self, document: DocumentMetadata) -> None:
        pass

    @abstractmethod
    def find_by_id(self, document_id: str) -> DocumentMetadata | None:
        pass

    @abstractmethod
    def find_by_hash(self, file_hash: str) -> DocumentMetadata | None:
        pass

    @abstractmethod
    def find_all(self) -> list[DocumentMetadata]:
        pass

    @abstractmethod
    def find_active(self) -> list[DocumentMetadata]:
        pass

    @abstractmethod
    def update_status(
        self,
        document_id: str,
        status: str
    ) -> None:
        pass

    @abstractmethod
    def exists(
        self,
        file_hash: str
    ) -> bool:
        pass
