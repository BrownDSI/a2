from collections import Counter
import time
from typing import List

import pandas as pd


def jaccard_similarity(a: str,
                       b: str,
                       token='letter',
                       k=1) -> float:
    """Takes in two strings and computes the Jaccard similarity of them.

    Consider ignoring case and removing punctuation

    Note: We will only be testing that fuzzy_match works correctly.
    """
    # TODO: Task 10
    # YOUR CODE HERE
    pass


def fuzzy_match(spotify_df: pd.DataFrame,
                lastfm_df: pd.DataFrame) -> List:
    """Takes in the spotify and lastfm dataframes and returns
    a list of songs with similar song names and artist names
    """
    # TODO: Task 10
    # YOUR CODE HERE
    pass


##############
# TEST CASES #
##############
def test_jaccard():
    assert jaccard_similarity('a', 'b') == 0
    assert jaccard_similarity('c', 'c') == 1
    assert jaccard_similarity('C', 'c') == 1
    assert jaccard_similarity('ace', 'acd') == 2 / 4
    # Consider using bigrams instead of letters
    assert jaccard_similarity('ace', 'acd', k=2) == 1 / 3


def test_fuzzy_match():
    spotify_df = (pd.read_csv('data/solutions/spotify.csv')
                  .sort_values('song_name')
                  .iloc[1000:1100])
    lastfm_df = (pd.read_csv('data/solutions/lastfm_t6.csv')
                 .sort_values('song_name')
                 .iloc[1700:1800])

    similar_songs = fuzzy_match(spotify_df, lastfm_df)
    assert isinstance(similar_songs, list)
    assert ('sippin’ on fire', 'sipping on fire') in similar_songs


if __name__ == '__main__':
    spotify_df = pd.read_csv('data/solutions/spotify.csv')
    lastfm_df = pd.read_csv('data/solutions/lastfm_t6.csv')

    # TODO: Task 10
    # Write your data from Fuzzy Match to data/similar_songs.csv
    print("Fuzzy match started")
    start2 = time.time()
    # YOUR CODE HERE
    end2 = time.time()
    print("Fuzzy match took", (end2 - start2) / 60, "minutes")
