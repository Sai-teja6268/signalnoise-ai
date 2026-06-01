import pandas as pd
from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument

class CSVLoader(BaseLoader):
    def load(self,file_path:str):
        df = pd.read_csv(file_path)
        docs=[]
        for index, row in df.iterrows():
            docs.append(
                EnterpriseDocument(
                    document_id=str(index),
                    source="csv",
                    content=row.get("message"),
                    team=row.get("team")
                )
            )
        return docs