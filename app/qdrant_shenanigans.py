from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.api import QDRANT_API_KEY, QDRANT_URL, COLLECTION_NAME

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY    
)

def create():
    client.create_collection(
        collection_name="ai_talent_docs",
        vectors_config=models.VectorParams(
            size=1536,  # размерность эмбеддера (len(embeddings.embed_query("test")))
            distance=models.Distance.COSINE
        )
    )

def drop():
    client.delete_collection(collection_name="ai_talent_docs")
    print("Коллекция удалена")



