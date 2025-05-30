from .providers import ChromaProvider
from .vdb_enums import VectorDBType
from config import settings

class VDBProviderFactory:
    def __init__(self):
        self.config = settings.vector_db_config

    def create(self, provider: str):
        if provider == VectorDBType.CHROMA.value:
            chroma_provider = ChromaProvider(
                db_path=self.config["path"],
                embedding_model=self.config["embedding_model"],
                distance_method=self.config["distance_method"],
                )
            return chroma_provider
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        