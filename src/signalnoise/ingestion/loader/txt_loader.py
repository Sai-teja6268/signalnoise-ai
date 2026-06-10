import uuid
from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument
from .metadata_extractor import extract_metadata

class TXTLoader(BaseLoader):
    def load(self, file_path:str):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
            
        meta = extract_metadata(data, file_path)
        
        return [
            EnterpriseDocument(
                document_id=str(uuid.uuid4()),
                source="txt",
                content=data,
                file_name=meta["file_name"],
                team=meta["team"],
                department=meta["department"],
                date=meta["date"]
            )
        ]