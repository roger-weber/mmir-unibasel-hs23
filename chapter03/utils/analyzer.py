from . import stopwords
import re, collections


def bag_of_words(text: str = None, tokens: list[str] = None, remove_stopwords: bool = True) -> dict[str, int]:
    freqs = collections.Counter(text and tokenize(text) or tokens)
    if remove_stopwords:
        for token in stopwords.english:
            del freqs[token]
    return dict(freqs)

def set_of_words(text: str = None, tokens: list[str] = None, remove_stopwords: bool = True) -> set[str]:
    freqs = collections.Counter(text and tokenize(text) or tokens)
    if remove_stopwords:
        for token in stopwords.english:
            del freqs[token]
    return set(freqs)

def tokenize(text: str) -> list[str]:
    text = re.sub(r'[,\.\-\?!\(\)\s:;_\'"\+\*\&\$]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text.split(' ')
