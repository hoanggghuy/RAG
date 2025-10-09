import os
from pdf2image import convert_from_path
import easyocr
import time
import numpy as np
import json  # <-- THÊM THƯ VIỆN JSON

print("Đang tải mô hình EasyOCR vào bộ nhớ...")
reader = easyocr.Reader(['vi', 'en'])
print("Tải mô hình thành công.")


def ocr_scanned_pdf(pdf_path: str, poppler_path: str = None):
    if not os.path.exists(pdf_path):
        return {"error": f"Không tìm thấy file tại đường dẫn '{pdf_path}'"}

    print(f"\nBắt đầu xử lý file: {os.path.basename(pdf_path)}")
    start_time = time.time()

    try:
        print("Bước 1/3: Đang chuyển đổi PDF thành ảnh...")
        if poppler_path:
            images = convert_from_path(pdf_path, poppler_path=poppler_path)
        else:
            images = convert_from_path(pdf_path)

        print(f"-> Chuyển đổi thành công {len(images)} trang.")

        print("Bước 2/3: Đang thực hiện OCR trên từng trang...")

        # --- THAY ĐỔI 1: Tạo một list để lưu dữ liệu của từng trang ---
        pages_data = []
        for i, image in enumerate(images):
            page_start_time = time.time()

            image_np = np.array(image)
            results = reader.readtext(image_np, detail=0, paragraph=True)
            page_text = "\n".join(results)

            # Thêm dữ liệu của trang vào list
            pages_data.append({
                "page_number": i + 1,
                "content": page_text
            })

            page_end_time = time.time()
            print(f"-> Hoàn thành OCR trang {i + 1}/{len(images)} trong {page_end_time - page_start_time:.2f} giây.")

        end_time = time.time()
        print("Bước 3/3: Hoàn tất quá trình OCR.")
        print(f"Tổng thời gian xử lý: {end_time - start_time:.2f} giây.")

        # --- THAY ĐỔI 2: Tạo và trả về đối tượng dictionary cuối cùng ---
        final_output = {
            "file_name": os.path.basename(pdf_path),
            "total_pages": len(images),
            "pages": pages_data
        }
        return final_output

    except Exception as e:
        return {"error": f"Đã xảy ra lỗi trong quá trình xử lý: {e}"}


if __name__ == '__main__':
    pdf_file_path = r"C:\Users\ADMIN\Desktop\DATK1\data\pdf\4.pdf"
    poppler_bin_path = r"C:\Users\ADMIN\Desktop\DATK1\Release-25.07.0-0\poppler-25.07.0\Library\bin"

    # Tên biến được đổi để rõ nghĩa hơn
    extracted_data = ocr_scanned_pdf(pdf_file_path, poppler_path=poppler_bin_path)

    print("\n--- KẾT QUẢ OCR (JSON) ---\n")
    # In ra JSON với định dạng đẹp
    print(json.dumps(extracted_data, indent=2, ensure_ascii=False))

    # --- THAY ĐỔI 3: Lưu kết quả ra file .json ---
    if "error" not in extracted_data:
        output_json_path = os.path.splitext(pdf_file_path)[0] + "_ocr_result.json"
        with open(output_json_path, "w", encoding="utf-8") as f:
            # Dùng json.dump để ghi dictionary vào file
            # ensure_ascii=False để hiển thị đúng tiếng Việt
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        print(f"\n-> Kết quả đã được lưu vào file: {output_json_path}")