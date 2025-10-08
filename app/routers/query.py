from fastapi import APIRouter
from app.services.search_service import search_qdrant
from pydantic import BaseModel

class Query(BaseModel):
    query: str
    top_k: int
router = APIRouter()
@router.post("/query")
def query_rag(query : Query):
    results = search_qdrant(query=query.query, top_k=query.top_k)
    return {"question": query.query, "results": results}
