import os
import pandas as pd
from typing import TypedDict

Document = TypedDict('Document', {'id': int, 'title': str, 'year': int, 'runtime': int, 'rating': float, 'genre': str, 'actors': str, 'summary': str})
DocumentCollection = list[Document]

def load() -> DocumentCollection:
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'imdb_top_1000.csv'))
    df.drop(['Poster_Link', 'Certificate', 'Meta_score', 'Director', 'No_of_Votes', 'Gross'], axis=1, inplace=True)

    # rename columns to produce dictionary
    df.rename(columns={'Series_Title': 'title'}, inplace=True)
    df.rename(columns={'Released_Year': 'year'}, inplace=True)
    df.rename(columns={'Runtime': 'runtime'}, inplace=True)
    df.rename(columns={'Genre': 'genre'}, inplace=True)
    df.rename(columns={'IMDB_Rating': 'rating'}, inplace=True)
    df.rename(columns={'Overview': 'summary'}, inplace=True)

    # replace content
    df['runtime'].replace(to_replace=r'(\d*) min', value=r'\1', regex=True, inplace=True)
    df['genre'].replace(r',', '', regex=True, inplace=True)
    df['actors'] = df[['Star1', 'Star2', 'Star3', 'Star4']].apply(lambda x: ' '.join(x), axis=1)

    # convert to target type
    df['runtime'] = df['runtime'].astype(int)
    df.drop(['Star1', 'Star2', 'Star3', 'Star4'], axis=1, inplace=True)

    # reorder columns
    df = df[['title', 'year', 'runtime', 'rating', 'genre', 'actors', 'summary']]

    # return dictionary
    return df.to_dict('records')

def format(doc: dict, row: list[str] = None) -> list[str]:
    trim = lambda s,n: len(s) > n and s[:n] + "\u2026" or s
    row = row or []
    row.append(str(doc.get('id', 0)))
    row.append(trim(doc['title'], 30))
    row.append(str(doc['year']))
    row.append(str(doc['runtime']))
    row.append(str(round(doc['rating'], 1)))
    row.append(trim(doc['genre'], 20))
    row.append(trim(doc['actors'], 30))
    row.append(trim(doc['summary'], 100))
    return row


def headers(*args: str) -> list[str]:
    headers = list(args)
    headers.append('id')
    headers.append('title')
    headers.append('year')
    headers.append('runtime')
    headers.append('rating')
    headers.append('genre')
    headers.append('actors')
    headers.append('summary')
    return headers
    
