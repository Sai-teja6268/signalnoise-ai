from pypdf import PdfReader
from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument
class PDFLoader(BaseLoader):
    def load(self,file_path:str):
        reader = PdfReader(file_path)
        text=""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return [
            EnterpriseDocument(
                document_id="1",
                source="pdf",
                content = text
            )
        ]