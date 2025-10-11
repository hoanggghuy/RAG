from sentence_transformers import SentenceTransformer
import os
import json
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

inp_dr = r"C:\Users\ADMIN\Desktop\DATK1\data\chunked_json"
out_dr = r"C:\Users\ADMIN\Desktop\DATK1\data\embedding"

os.makedirs(out_dr, exist_ok=True)
def process_embedding(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "text" in data:
        texts = data["text"]
    elif isinstance(data, list):
        texts = data
    else:
        raise TypeError("Invalid data type")
    embedding = []
    for item in texts:
        text = item["chunk"]
        page =item.get("page", None)
        embed = model.encode(text).tolist()
        embedding.append(
            {
                "page": page,
                "chunk": text,
                "embed": embed,
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