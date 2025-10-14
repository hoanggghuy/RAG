from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.services.embed_service import embedding_query
from app.config import get_settings
from sentence_transformers import CrossEncoder
settings = get_settings()
Collection_Name = settings.COLLECTION_NAME
cross_encoder = CrossEncoder('Alibaba-NLP/gte-multilingual-base',
                             trust_remote_code=True)
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
            "text" : hit.payload.get("page_content") if "page_content" in hit.payload else None,
        }
        )
    pairs =[]
    for result in results:
        pairs.append([query,result["text"]])
    new_scores = cross_encoder.predict(pairs)
    for i in range(len(results)):
        results[i]["new_score"] = float(new_scores[i])
    results.sort(key=lambda x: x['new_score'], reverse=True)
    return results