import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
def process_chunk(file_path: str, output_path: str):
    global texts
    if not os.path.exists(file_path):
        print("File doesn't exist")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    texts = []
    if isinstance(data, dict) and "pages" in data:
        for page in data["pages"]:
            texts.append({
                "page" : page["page_number"],
                "content" : page["content"],
            })
    if isinstance(data, list) :
        for i in range(len(data)):
            texts.append({
                "metadata" : {
                    "product_name" : data[i]["metadata"]["product_name"],
                    "source_url" : data[i]["metadata"]["source_url"],
                    "category" : data[i]["metadata"]["category"],
                },
                "page_content" : data[i]["page_content"],
            })
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    chunks = []
    for item in texts:
        page_content = item["page_content"]
        if item["metadata"]["category"] == "Thông tin chi tiết sản phẩm":
            for chunk in splitter.split_text(page_content):
                chunks.append({
                    "metadata" : item["metadata"],
                    "page_content" : chunk,
                })
        else:
            chunks.append({
                "metadata" : item["metadata"],
                "page_content" : page_content,
            })
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f,ensure_ascii=False,indent=4)

if __name__ == "__main__":
    a = r"../../data/embedding/rag_documents_grouped.json"
    b= r"C:\Users\ADMIN\Desktop\DATK1\data\chunked_json\output6.json"
    process_chunk(a, b)