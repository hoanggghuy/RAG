import os
from pdf2image import convert_from_path
import easyocr
import json
from regex_service import Regex
reader = easyocr.Reader(['vi','en'])

def ocr_scanned_pdf(pdf_file_path: str, popler_path: str, output_path: str):
    if not os.path.exists(pdf_file_path):
        return print("Not found path")
    os.makedirs(output_path, exist_ok=True)
    try:
        if popler_path:
            images = convert_from_path(pdf_file_path, poppler_path=popler_path, dpi= 300)
        else:
            images = convert_from_path(pdf_file_path)
        page_data = []
        for i, image in enumerate(images):
            image_path = os.path.join(output_path, f"{i}.jpg")
            image.save(image_path,"JPEG")
            results = reader.readtext(image_path, detail=0, paragraph=True)
            page_text = "\n".join(results)
            page_text = Regex(page_text)
            page_data.append({
                "page_number": i+1,
                "content": page_text
            })
        final_output = {
            "file_name": pdf_file_path,
            "total_page" : len(images),
            "pages" : page_data,
        }
        return final_output

    except Exception as e:
        print(e)
def Regex_JSON(json_file_path: str):
    with open(json_file_path,"r",encoding="utf-8") as f:
        data = json.load(f)
    for page in data.get("pages", []):
        content = page["content"]
        page["content"] = Regex(content)
    with open(json_file_path,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

if __name__ == '__main__':
    pdf_path = r"C:\Users\ADMIN\Desktop\DATK1\data\pdf\4.pdf"
    popler_path = r"C:\Users\ADMIN\Desktop\DATK1\Release-25.07.0-0\poppler-25.07.0\Library\bin"
    output_path = r"C:\Users\ADMIN\Desktop\DATK1\data\Pic"
    output_json_path = r"C:\Users\ADMIN\Desktop\DATK1\data\json\output4.json"
    data = ocr_scanned_pdf(pdf_file_path=pdf_path, popler_path=popler_path, output_path=output_path)
    if "error"  not in data:
        output_json_path = output_json_path
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    Regex_JSON(output_json_path)