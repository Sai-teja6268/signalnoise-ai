import json
import uuid
import os
from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument
from .metadata_extractor import extract_metadata

class JSONLoader(BaseLoader):
    def load(self,file_path:str):
        with open(file_path,'r') as f:
            data = json.load(f)
        file_name = os.path.basename(file_path)
        docs = []
        for index, item in enumerate(data):
            content = item.get("message") or item.get("content") or ""
            if not isinstance(content, str):
                content = str(content)
            if not content:
                content = ", ".join(f"{k}: {v}" for k, v in item.items() if v is not None)
                
            meta = extract_metadata(content, file_path)
            
            team = item.get("team") or meta["team"]
            department = item.get("department") or meta["department"]
            date = item.get("date") or meta["date"]

            docs.append(
                EnterpriseDocument(
                    document_id=str(uuid.uuid4()),
                    source="json",
                    content=content,
                    file_name=file_name,
                    team=str(team) if team else None,
                    department=str(department) if department else None,
                    date=str(date) if date else None
                )
            )
        return docs
