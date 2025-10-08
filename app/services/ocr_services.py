import fitz
import pytesseract
from PIL import Image
import io
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import json
import re
from regex_service import normalize

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ADMIN\Desktop\tess\tesseract.exe'

def ocr_page (pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=300)
    img =Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang='vie')
    doc.close()
    return page_num + 1 ,text.strip()
def ocr_pdf_parallel (pdf_path, max_workers = None):
    doc = fitz.open(pdf_path)
    total_page = len(doc)
    doc.close()
    result = []
    if max_workers is None:
        max_workers = os.cpu_count() // 2 + 1
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(ocr_page, pdf_path, i) for i in range(total_page)]
        for future in as_completed(futures):
            page_num, text = future.result()
            result.append({'page':page_num, 'text':text})
        for _ in result:
            _['text'] = re.sub("\\n+.", " ",normalize(_['text']))
            _['text'] =  re.sub('—', "",_['text'])
            _['text'] = re.sub(r"\d+\.\s|\d+\d|([A-Za-z0-9\-]+\.(?:com|net|org|vn))|(https?://[\S]+)", "", _['text'])
            _['text'] = _['text'].replace("\\u003C", "<").replace("\\u003E", ">").replace("\\u0026", "&")

    result.sort(key=lambda x:x['page'])
    return result
if __name__ == '__main__':
    pdf_path = r"C:\Users\ADMIN\Desktop\DATK1\data\pdf\4.pdf"
    output = ocr_pdf_parallel(pdf_path)

    # for page in output:
    #     print(f"\n--- Page {page['page']} ---\n{page['text']}")
    json_str = json.dumps(output, ensure_ascii=False, indent=4)
    with open("../../data/json/output.json", "w", encoding="utf-8") as f:
        f.write(json_str)
    print(json_str)