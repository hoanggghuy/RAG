from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.services.embed_service import embedding_query
from app.config import get_settings
settings = get_settings()
Collection_Name = settings.COLLECTION_NAME

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
def search_qdrant(query:str, top_k: int =3):
    query_vector = embedding_query(query)
    hits= client.query_points(
        collection_name=Collection_Name,
        query=query_vector,
        limit=top_k,
    )
    results = []
    for hit in hits.points:
        results.append({
            "score" : hit.score,
            "text" : hit.payload.get("Context") if "Context" in hit.payload else None,
        }
        )
    return results
