import json
import re
import os


def clean_text(text: str) -> str:
    """
    Hàm này nhận một chuỗi văn bản và áp dụng các quy tắc làm sạch.
    """
    # Quy tắc 1: Thay thế nhiều ký tự xuống dòng hoặc khoảng trắng bằng một khoảng trắng duy nhất.
    # re.sub(r'\s+', ' ', text) là cách an toàn và hiệu quả hơn.
    cleaned_text = re.sub(r'\s+', ' ', text)

    # Quy tắc 2: Xóa ký tự gạch ngang dài (em dash)
    cleaned_text = re.sub('—', '', cleaned_text)

    # Quy tắc 3: Xóa các mục liệt kê bằng số, số có nhiều hơn 2 chữ số,
    # tên miền (domain) và đường dẫn URL.
    # \d{2,} sẽ tìm các số có 2 chữ số trở lên.
    pattern_to_remove = r"\d+\.\s|\d{2,}|([A-Za-z0-9\-]+\.(?:com|net|org|vn))|(https?://[\S]+)"
    cleaned_text = re.sub(pattern_to_remove, "", cleaned_text)
    cleaned_text = cleaned_text.replace("\\u003C", "<").replace("\\u003E", ">").replace("\\u0026", "&").replace("[-]", " ")
    # Quy tắc 4: Thay thế các chuỗi unicode escape.
    # Thường thì json.load đã xử lý việc này, nhưng ta vẫn thêm vào theo yêu cầu.
    cleaned_text = cleaned_text.replace("\\u003C", "<").replace("\\u003E", ">").replace("\\u0026", "&")

    # Trả về văn bản đã được làm sạch và loại bỏ khoảng trắng thừa ở đầu/cuối
    return cleaned_text.strip()


def process_json_file(input_path: str, output_path: str):
    """
    Hàm chính để đọc, xử lý và ghi file JSON.
    """
    try:
        # 1. Đọc file JSON đầu vào
        print(f"Đang đọc dữ liệu từ: {input_path}")
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 2. Lặp qua từng trang và làm sạch nội dung
        print("Bắt đầu quá trình làm sạch văn bản...")
        if 'pages' in data and isinstance(data['pages'], list):
            for page in data['pages']:
                if 'content' in page and isinstance(page['content'], str):
                    original_content = page['content']
                    cleaned_content = clean_text(original_content)
                    page['content'] = cleaned_content

        # 3. Ghi dữ liệu đã được làm sạch vào file JSON mới
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Hoàn tất! Dữ liệu đã được làm sạch và lưu vào: {output_path}")

    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file đầu vào tại '{input_path}'")
    except json.JSONDecodeError:
        print(f"❌ Lỗi: File '{input_path}' không phải là một file JSON hợp lệ.")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi không mong muốn: {e}")


# --- PHẦN THỰC THI CHÍNH ---
if __name__ == '__main__':
    # THAY ĐỔI CÁC ĐƯỜNG DẪN DƯỚI ĐÂY

    # Đường dẫn đến file JSON kết quả OCR của bạn
    input_file = r"C:\Users\ADMIN\Desktop\DATK1\data\pdf\4_ocr_result.json"

    # Tên file JSON mới sau khi đã làm sạch
    output_file = r"C:\Users\ADMIN\Desktop\DATK1\data\json\output3.json"

    # Gọi hàm xử lý chính
    process_json_file(input_path=input_file, output_path=output_file)