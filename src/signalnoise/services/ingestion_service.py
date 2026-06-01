from signalnoise.ingestion.loader_factory import loadFacory

class IngestionService:
    def ingest(self, file_path:str):
        loader = loadFacory.get_loader(file_path)
        documents = loader.load(file_path)
        return documents