import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
                "page" : data[i]["metadata"]["source"],
                "content" : data[i]["page_content"],
            })
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = []
    for item in texts:
        content = item["content"]
        for chunk in splitter.split_text(content):
            chunks.append({
                "page": item["page"],
                "chunk": chunk,
            })
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f,ensure_ascii=False,indent=4)

if __name__ == "__main__":
    a = r"../../data/data_crawl/Crawl_Data.json"
    b= r"C:\Users\ADMIN\Desktop\DATK1\data\chunked_json\output=5.json"
    process_chunk(a, b)