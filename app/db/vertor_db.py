import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
import json
from app.config import settings

Collection_Name = settings.COLLECTION_NAME
Embedding_Dir = settings.EMBEDDING_DIR
def connect_qdrant_client():
    client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
    return client
def init_collection(vector_size =384):
    connect_qdrant_client().create_collection(
        collection_name=Collection_Name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )
def load_embedding():
    embedding =[]
    for filename in os.listdir(Embedding_Dir):
        if filename.endswith(".json"):
            with open(os.path.join(Embedding_Dir, filename), "r", encoding="utf-8") as f:
                embedding.extend(json.load(f))

    return embedding
def insert_embedding(embeddings, collection_name=Collection_Name):
    points = []
    for idx, item in enumerate(embeddings):
        points.append(
            models.PointStruct(
                id=item.get("id", idx),
                vector=list(item["embed"]),
                payload={
                    "page": item.get("page"),
                    "text": item.get("text"),
                }
            )
        )

    connect_qdrant_client().upsert(
        collection_name=collection_name,
        wait=True,
        points=points,
    )




if __name__ == '__main__':
    init_collection()
    embedding = load_embedding()
    insert_embedding(embedding)