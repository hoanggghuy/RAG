from sentence_transformers import SentenceTransformer
import os
import json
from pathlib import Path
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

inp_dr = r"C:\Users\ADMIN\Desktop\DATK1\data\chunked_json"
out_dr = r"C:\Users\ADMIN\Desktop\DATK1\data\Data_to_db"

os.makedirs(out_dr, exist_ok=True)
def process_embedding(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        texts = json.load(f)
    # if isinstance(data, dict) and "page_content" in data:
    #     texts = data["page_content"]
    # elif isinstance(data, list):
    #     texts = data
    # else:
    #     raise TypeError("Invalid data type")
    embedding = []
    for item in texts:
        text = item["page_content"]
        embed = model.encode(text).tolist()
        embedding.append(
            {
                "metadata" : item["metadata"],
                "page_content" : item["page_content"],
                "embedding" : embed,
            }
        )
    return embedding
def embedding_query(query:str):
    embedded_query = model.encode(query).tolist()
    return embedded_query
def main():
    for fname in os.listdir(inp_dr):
        if fname.endswith(".json"):
            fpath = os.path.join(inp_dr, fname)
            embedding = process_embedding(fpath)
            out_path = os.path.join(out_dr, fname)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(embedding, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()