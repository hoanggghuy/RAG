from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.services.embed_service import embedding_query

COLLECTION_NAME = "datachatbot"

client = QdrantClient(url="http://localhost:6333")
def search_qdrant(query:str, top_k: int =3):
    query_vector = embedding_query(query)
    hits= client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )
    results = []
    for hit in hits.points:
        results.append({
            "score" : hit.score,
            "page" : hit.payload.get("page") if "page" in hit.payload else None,
            "text" : hit.payload.get("text") if "text" in hit.payload else None,
        }
        )
    return results
