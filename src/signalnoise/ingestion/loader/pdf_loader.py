import uuid
from pypdf import PdfReader
from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument
from .metadata_extractor import extract_metadata

class PDFLoader(BaseLoader):
    def load(self,file_path:str):
        reader = PdfReader(file_path)
        text=""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        meta = extract_metadata(text, file_path)
        
        return [
            EnterpriseDocument(
                document_id=str(uuid.uuid4()),
                source="pdf",
                content=text,
                file_name=meta["file_name"],
                team=meta["team"],
                department=meta["department"],
                date=meta["date"]
            )
        ]