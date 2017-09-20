import os
from urllib.parse import urljoin

import re
from typing import List, Dict

import pandas as pd


def prune_artists(artist_names: pd.Series) -> pd.Series:
    """Takes in a Series of artist names and returns a new Series
    with only the names of the first artist in each string/row.
    Some of the strings in artist_names refer to two or more
    artists.
    """
    # TODO: Task 9
    # YOUR CODE HERE
    pass


def clean_billboard(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans Billboard items collected by BillboardCrawler

    Note: This function takes in a DataFrame, not a list.
    """
    pruned_col = prune_artists(df['artist_names'])
    cleaned_df: pd.DataFrame = (df.assign(main_artist_name=pruned_col)
                                .drop_duplicates()
                                .dropna()
                                .drop('artist_names', axis=1))
    return cleaned_df


def view_pruned(pruned: pd.Series, file_path: str) -> None:
    """Saves the column to a CSV file. As the column is sorted,
    it is easier to see errors through this file. Use this function to
    help you debug your prune_artists implementation"""
    (pruned
     .sort_values()
     .drop_duplicates()
     .to_csv(file_path, index=False))


##############
# TEST CASES #
##############
def test_prune_dummy():
    """Tests prune_artists_col on dummy data.
    """
    dummy1 = pd.Series(data=['Major Lazer & DJ Snake Featuring MO'])
    pruned1 = prune_artists(dummy1)
    assert pruned1[0] == 'major lazer'
    dummy2 = pd.Series(data=['Selena Gomez Featuring A$AP Rocky',
                             ('Macklemore & Ryan Lewis Featuring Eric Nally,' +
                              'Melle Mel, Kool Moe Dee & Grandmaster Caz'),
                             'Young Thug And Travis Scott Featuring Quavo'])
    pruned2 = prune_artists(dummy2)
    assert pruned2[0] == 'selena gomez'
    assert pruned2[1] == 'macklemore'
    assert pruned2[2] == 'young thug'


def test_prune_full():
    abs_path = urljoin(os.getcwd(),
                       'a2-data-wrangling/data/solutions/hot100.csv')
    df = pd.read_csv(abs_path)
    df_copy = df.copy()

    pruned_col = prune_artists(df['artist_names'])

    assert pruned_col.str.contains(' and ').any() == False
    assert pruned_col.str.contains('&').any() == False
    assert pruned_col.str.contains(' featuring').any() == False


def test_clean_partial():
    abs_path = urljoin(os.getcwd(),
                       'a2-data-wrangling/data/solutions/hot100.csv')
    df = pd.read_csv(abs_path)
    df_copy = df.copy()

    cleaned = clean_billboard(df.iloc[0:10])

    assert 'rank' in cleaned.columns
    assert 'week' in cleaned.columns
    assert not cleaned['main_artist_name'].empty
    assert not df.isnull().values.any()
    assert not df.duplicated().any()
    assert df.equals(df_copy)


def test_clean_full():
    abs_path = urljoin(os.getcwd(),
                       'a2-data-wrangling/data/solutions/hot100.csv')
    df = pd.read_csv(abs_path)
    df_copy = df.copy()

    cleaned = clean_billboard(df)

    assert not cleaned['main_artist_name'].empty
    assert not df.isnull().values.any()
    assert not df.duplicated().any()
    assert df.equals(df_copy)

if __name__ == '__main__':
    abs_path = urljoin(os.getcwd(),
                       'a2-data-wrangling/data/solutions/hot100.csv')
    df = pd.read_csv(abs_path)

    cleaned = clean_billboard(df)
    cleaned.to_csv('data/hot100_clean.csv', index=False)