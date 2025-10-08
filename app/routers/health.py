from fastapi import APIRouter
from app.db.vertor_db import connect_qdrant_client
router = APIRouter()

@router.get("/health")
async def health():
    try:
        qdrant_client = connect_qdrant_client()
        qdrant_client.get_collections()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}