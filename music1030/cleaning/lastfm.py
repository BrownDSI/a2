import re

import numpy as np
import pandas as pd


def split_songs(songs: pd.Series) -> (pd.Series, pd.Series):
    # TODO: Task 6
    # YOUR CODE HERE
    pass


def clean_lastfm(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the Last.fm data set by:

        shifting down and the songs column,
        dropping rows with null values,
        splitting the song column into the song and artist names, and
        removing songs with the same name and artist

    """
    cleaned_df: pd.DataFrame = df.copy()
    # Shift the songs column
    toptags_col = cleaned_df.columns[2]
    cleaned_df[toptags_col] = cleaned_df[toptags_col].shift(1)
    cleaned_df.loc[0, toptags_col] = toptags_col
    cleaned_df.rename(columns={cleaned_df.columns[2]: 'toptags'}, inplace=True)

    # Dropped nulls
    cleaned_df.dropna(inplace=True)

    # Split the song column
    cleaned_df['song_name'], cleaned_df['main_artist_name'] = split_songs(
        cleaned_df['song'])

    # Remove duplicate songs, keeping the most popular
    cleaned_df.sort_values(by='listeners',
                           inplace=True,
                           ascending=False)
    cleaned_df.drop_duplicates(subset=['song_name', 'main_artist_name'],
                               inplace=True)

    return cleaned_df.drop('song', axis=1)


def reshape_lastfm(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: Task 7
    # YOUR CODE HERE
    pass


##############
# TEST CASES #
##############
def test_split_songs():
    s = pd.Series(
        data=['This is the song "No I in Threesome" by artist "Interpol"',
              '2 Trees [Foals]'])

    songs, artists = split_songs(s)

    # "This is the song ""No I in Threesome"" by artist ""Interpol"""
    assert songs[0] == 'no i in threesome'
    assert artists[0] == 'interpol'

    # 2 Trees [Foals]
    assert songs[1] == '2 trees'
    assert artists[1] == 'foals'


def test_clean():
    df = pd.read_csv('data/lastfm.csv').iloc[0:10]
    df_copy = df.copy()
    cleaned = clean_lastfm(df)

    assert 'alternative:100' in cleaned.iloc[0]['toptags']
    assert not cleaned.isnull().values.any()
    assert not cleaned.duplicated(
        subset=['song_name', 'main_artist_name']).any()
    assert df.equals(df_copy)


def test_reshape():
    df = pd.read_csv('data/solutions/lastfm_t6.csv').iloc[0:10]
    df_copy = df.copy()

    assert df.equals(df_copy)


if __name__ == '__main__':
    import os
    from urllib.parse import urljoin

    abs_path = urljoin(os.getcwd(), 'a2-data-wrangling/data')
    df = pd.read_csv(os.path.join(abs_path, 'lastfm.csv'))

    cleaned = clean_lastfm(df)
    cleaned.to_csv(os.path.join(abs_path, 'lastfm_t6.csv'), index=False)

    reshaped = reshape_lastfm(cleaned)
    reshaped.to_csv(os.path.join(abs_path, 'lastfm_t7.csv'), index=False)
