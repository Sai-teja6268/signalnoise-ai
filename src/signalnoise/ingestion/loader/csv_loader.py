import uuid
import pandas as pd
import os
from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument
from .metadata_extractor import extract_metadata

class CSVLoader(BaseLoader):
    def load(self,file_path:str):
        df = pd.read_csv(
            file_path,
            quotechar='"',
            on_bad_lines='skip',
            encoding='utf-8',
            engine='python'
        )
        file_name = os.path.basename(file_path)
        docs=[]
        for index, row in df.iterrows():
            content = row.get("message") or row.get("content") or ""
            if not isinstance(content, str):
                content = str(content)
            if not content:
                content = ", ".join(f"{k}: {v}" for k, v in row.items() if pd.notna(v))
                
            meta = extract_metadata(content, file_path)
            
            team = row.get("team") or meta["team"]
            department = row.get("department") or meta["department"]
            date = row.get("date") or meta["date"]
            
            if pd.isna(team):
                team = meta["team"]
            if pd.isna(department):
                department = meta["department"]
            if pd.isna(date):
                date = meta["date"]

            docs.append(
                EnterpriseDocument(
                    document_id=str(uuid.uuid4()),
                    source="csv",
                    content=content,
                    file_name=file_name,
                    team=str(team) if pd.notna(team) and team else None,
                    department=str(department) if pd.notna(department) and department else None,
                    date=str(date) if pd.notna(date) and date else None
                )
            )
        return docs