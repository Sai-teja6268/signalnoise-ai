from pathlib import Path

from .loader.csv_loader import CSVLoader
from .loader.docx_loader import DOCXLoader
from .loader.json_loader import JSONLoader
from .loader.pdf_loader import PDFLoader
from .loader.txt_loader import TXTLoader

class loadFacory:
    @staticmethod
    def get_loader(file_path:str):
        extension = Path(file_path).suffix.lower()

        mapping ={
            ".csv":CSVLoader,
            ".pdf":PDFLoader,
            ".txt":TXTLoader,
            ".docx":DOCXLoader,
            ".json":JSONLoader
        }

        loader = mapping.get(extension)
        if not loader:
            raise ValueError(
                f"Unsupported filetype: {extension} "
            )
        return loader()
        