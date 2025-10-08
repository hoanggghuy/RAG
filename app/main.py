from fastapi import FastAPI
from app.routers import query, health

app = FastAPI(title="RAG")

app.include_router(query.router, prefix="/query", tags=["query"])
@app.get("/")
async def root():
    return {"message": "Chatbot is running!"}
app.include_router(health.router, prefix="/api")
