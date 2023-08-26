from . import stopwords
from itertools import groupby
import re


def bag_of_words(text: str = None, tokens: list[str] = None, remove_stopwords: bool = True) -> dict[str, int]:
    if text is not None:
        tokens = tokenize(text)
    if remove_stopwords:
        tokens = [token for token in tokens if token not in stopwords.english]
    return dict([(token, len(list(group))) for token, group in groupby(sorted(tokens))])

def set_of_words(text: str = None, tokens: list[str] = None, remove_stopwords: bool = True) -> set[str]:
    if text is not None:
        tokens = tokenize(text)
    if remove_stopwords:
        tokens = [token for token in tokens if token not in stopwords.english]
    return set([token for token, _ in groupby(sorted(tokens))])

def tokenize(text: str) -> list[str]:
    text = re.sub(r'[,\.\-\?!\(\)\s:;_\'"\+\*\&\$]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text.split(' ')
