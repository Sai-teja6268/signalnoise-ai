import json
from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument
class JSONLoader(BaseLoader):
    def load(self,file_path:str):
        with open(file_path,'r') as f:
            data = json.load(f)
        docs = []
        for index, item in enumerate(data):
            docs.append(
                EnterpriseDocument(
                    document_id=str(index),
                    source="json",
                    content=item.get("message"),
                    team=item.get("team")
                )
            )
        return docs
