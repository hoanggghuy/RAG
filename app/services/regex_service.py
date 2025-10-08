import re
SUPERSCRIPT_MAP = {
    ord("⁰"): "0", ord("¹"): "1", ord("²"): "2", ord("³"): "3", ord("⁴"): "4",
    ord("⁵"): "5", ord("⁶"): "6", ord("⁷"): "7", ord("⁸"): "8", ord("⁹"): "9",
    ord("⁺"): "+", ord("⁻"): "-", ord("ⁿ"): "n", ord("ⁱ"): "i",
}

SUBSCRIPT_MAP = {
    ord("₀"): "0", ord("₁"): "1", ord("₂"): "2", ord("₃"): "3", ord("₄"): "4",
    ord("₅"): "5", ord("₆"): "6", ord("₇"): "7", ord("₈"): "8", ord("₉"): "9",
    ord("₊"): "+", ord("₋"): "-", ord("₌"): "=", ord("₍"): "(", ord("₎"): ")",
}

EXTRA_MAP = {
    ord("º"): "o",   # hoặc "0" tùy ngữ cảnh
    ord("ª"): "a",
    ord("ð"): "d",
}
TRANSLATION_TABLE = {**SUPERSCRIPT_MAP, **SUBSCRIPT_MAP, **EXTRA_MAP}
def normalize(text:str)->str:
    return text.translate(TRANSLATION_TABLE)
def Regex(text):
    text = re.sub("\\n", " ",text)
    text = text.replace("\\u003C", "<").replace("\\u003E", ">").replace("\\u0026", "&").replace("[-]", " ")
    return text


