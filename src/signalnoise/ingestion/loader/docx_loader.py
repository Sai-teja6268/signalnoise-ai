from docx import Document
from .base_loader import BaseLoader
from signalnoise.ingestion.schema import EnterpriseDocument
class DOCXLoader(BaseLoader):
    def load(self,file_path:str):
        doc = Document(file_path)
        text = "\n".join(
            para.text for para in doc.paragraphs
        )
        return[
            EnterpriseDocument(
                document_id = "1",
                source="docx",
                content=text
            )
        ]