import hashlib
import re


def generate_md5_from_title(title: str) -> str:
    normalized = normalize_title(title)

    return hashlib.md5(normalized.encode()).hexdigest()


def normalize_title(title):
    normalized_title = re.sub(r'[^\w\u4e00-\u9fff]', '', title)
    normalized_title = normalized_title.lower()

    return normalized_title


def fullwidth_to_halfwidth(text):
    """全形轉半形"""
    translation_table = str.maketrans("！＠＃＄％＾＆＊（）＿：？", "!@#$%^&*()_:?")

    return text.translate(translation_table)
