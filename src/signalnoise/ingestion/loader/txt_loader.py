from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument
class TXTLoader(BaseLoader):
    def load(self, file_path:str):
        with open(file_path,'r',encoding='utf-8') as f:
            data = f.read()
        return[
            EnterpriseDocument(
                document_id = "1",
                source="txt",
                content=data
            )
        ]
        