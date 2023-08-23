import random
from typing import TypedDict

Document = TypedDict('Document', {'id': int, 'text': str})
DocumentCollection = list[Document]

def load(nDocs = 100, nTerms = 1) -> DocumentCollection:
    # create a set of documents with random number of terms
    terms = ['dog', 'cat', 'horse', 'rabit', 'ostrich', 'bear', 'tiger', 'lion', 'bird']
    dfs = [nDocs * max(int(100 // (i + 3) ** 0.5), 1) // 100 for i, _ in enumerate(terms)]
    index = [[] for _ in range(nDocs)]
    for term, df in zip(terms, dfs):
        for i in sorted(random.sample(range(nDocs), df)):
            tf = random.randint(1, nTerms)
            index[i].extend([term] * tf)
    
    # create the collection
    return [{'text': ' '.join(index[doc_id - 1])} for doc_id in range(1, nDocs + 1)]
