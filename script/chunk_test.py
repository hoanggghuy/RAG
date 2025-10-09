import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document


def chunk_data_from_json(json_path: str, output_path: str):
    """
    Đọc dữ liệu từ file JSON, chia nhỏ văn bản và lưu kết quả ra một file JSON mới.
    """
    try:
        # 1. Đọc file JSON đầu vào
        print(f"Đang đọc dữ liệu từ: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'pages' not in data:
            print("Lỗi: File JSON không có key 'pages'.")
            return

        # 2. Chuẩn bị dữ liệu cho LangChain
        print("Chuẩn bị dữ liệu từ các trang...")
        docs = []
        file_name = data.get("file_name", os.path.basename(json_path))
        for page_data in data['pages']:
            doc = Document(
                page_content=page_data.get('content', ''),
                metadata={
                    "source": file_name,
                    "page": page_data.get('page_number', 0)
                }
            )
            docs.append(doc)

        # 3. Khởi tạo Text Splitter
        print("Khởi tạo RecursiveCharacterTextSplitter...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )

        # 4. Chia nhỏ các Document
        print("Bắt đầu quá trình chunking...")
        chunks = text_splitter.split_documents(docs)
        print(f"✅ Hoàn tất! Đã chia thành công {len(chunks)} chunks.")

        # 5. Chuyển đổi các đối tượng Document thành dictionary để lưu file JSON
        chunks_to_save = [
            {"page_content": chunk.page_content, "metadata": chunk.metadata}
            for chunk in chunks
        ]

        # 6. Lưu kết quả ra file JSON mới
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunks_to_save, f, indent=2, ensure_ascii=False)

        print(f"-> Kết quả chunking đã được lưu vào file: {output_path}")

    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file tại '{json_path}'")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi không mong muốn: {e}")


# --- PHẦN THỰC THI CHÍNH ---
if __name__ == '__main__':
    # THAY ĐỔI CÁC ĐƯỜNG DẪN DƯỚI ĐÂY

    # Đường dẫn đến file JSON đã được làm sạch
    cleaned_json_file = r"C:\Users\ADMIN\Desktop\DATK1\data\json\output3.json"

    # Tên file JSON mới sẽ chứa các chunk
    chunked_output_file = os.path.splitext(cleaned_json_file)[0] + "_chunked.json"

    # Gọi hàm để thực hiện chunking và lưu file
    chunk_data_from_json(json_path=cleaned_json_file, output_path=chunked_output_file)

    print("\n--- QUY TRÌNH HOÀN TẤT ---")