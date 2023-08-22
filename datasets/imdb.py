import os
import pandas as pd

def load(type = 'dict'):
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
    df['summary'].replace(r'[,.!?-]', '', regex=True, inplace=True)
    df['actors'] = df[['Star1', 'Star2', 'Star3', 'Star4']].apply(lambda x: ' '.join(x), axis=1)
    df['id'] = df.index + 1

    # convert to target type
    df['runtime'] = df['runtime'].astype(int)
    df.drop(['Star1', 'Star2', 'Star3', 'Star4'], axis=1, inplace=True)

    # reorder columns
    df = df[['id', 'title', 'year', 'runtime', 'rating', 'genre', 'actors', 'summary']]

    # return dictionary
    if type == 'dict':
        return df.to_dict('records')
    return df


