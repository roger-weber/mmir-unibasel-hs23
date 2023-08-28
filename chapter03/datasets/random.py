import random

def load(nDocs = 100, nTerms = 5) -> list[dict]:
    # create a set of documents with random number of terms
    terms = ['dog', 'cat', 'horse', 'rabit', 'ostrich', 'bear', 'tiger', 'lion', 'bird', 'donkey', 'bee', 'ant' , 'fly', 'wale', 'snake']
    dfs = [nDocs * max(int(80 // (i + 4) ** 0.7), 1) // 100 for i, _ in enumerate(terms)]
    index = [[] for _ in range(nDocs)]
    for term, df in zip(terms, dfs):
        for i in sorted(random.sample(range(nDocs), df)):
            tf = random.randint(1, nTerms)
            index[i].extend([term] * tf)
    # create the collection
    return [{'text': ' '.join(index[doc_id - 1]) or 'fish'} for doc_id in range(1, nDocs + 1)]

def format(doc: dict, row: list[str] = None) -> list[str]:
    row = row or []
    row.append(str(doc.get('id')))
    row.append(doc.get('text'))
    return row


def headers(*args: str) -> list[str]:
    headers = list(args)
    headers.append('id')
    headers.append('text')
    return headers