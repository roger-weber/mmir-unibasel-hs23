import random

def load(nDocs = 100, nTerms = 1) -> list[dict]:
    # create a set of documents with random number of terms
    terms = ['dog', 'cat', 'horse', 'rabit', 'ostrich', 'bear', 'tiger', 'lion', 'bird', 'donkey', 'bee', 'ant']
    dfs = [nDocs * max(int(100 // (i + 4) ** 0.7), 1) // 100 for i, _ in enumerate(terms)]
    index = [[] for _ in range(nDocs)]
    for term, df in zip(terms, dfs):
        for i in sorted(random.sample(range(nDocs), df)):
            tf = random.randint(1, nTerms)
            index[i].extend([term] * tf)
    # create the collection
    return [{'text': ' '.join(index[doc_id - 1]) or 'fish'} for doc_id in range(1, nDocs + 1)]

def format(doc: dict, doc_id: int = None, score: float = None) -> str:
    doc_id = doc.get('id', doc_id)
    row = []
    if doc_id: row.append(doc_id)
    if score: row.append(score)
    row.append(doc.get('text'))
    return row


def headers(*args: str) -> list[str]:
    headers = list(args)
    headers.append('text')
    return headers