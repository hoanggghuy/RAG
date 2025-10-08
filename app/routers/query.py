from fastapi import APIRouter
from app.services.search_service import search_qdrant

router = APIRouter()
@router.post("/query")
def query_rag(question: str, top_k: int = 3):
    results = search_qdrant(question)
    return {"question": question, "results": results}
