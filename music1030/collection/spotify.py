import base64
import json
import time
from typing import Dict, List

import requests


class SpotifyCrawler():
    """A Spotify API crawler.

    Instantiate a SpotifyCrawler with your client ID and client
    secret then run the .search() or .crawl() methods to collect
    data.
    """

    def __init__(self,
                 client_id,
                 client_secret,
                 max_depth=25):
        self.access_token = self.get_new_token(client_id, client_secret)

        self.items = []
        self.max_depth = max_depth

    def search(self,
               query: str,
               item_type='track',
               limit=20):

        """Gets at most the first max_depth * limit items that match
        the input query and item type and stores them in self.items as Python
        dictionaries.
        """
        # TODO: Task 1 and Task 2
        offset = 0
        current_depth = 0

        while current_depth < self.max_depth:
            params = {
                'q': query,
                'type': 'track',
                'limit': limit,
                'offset': offset,
            }
            headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            r = requests.get('https://api.spotify.com/v1/search',
                             params=params,
                             headers=headers)

            if r.status_code == 200:
                new_items = r.json()['tracks']['items']
                self.items.extend(new_items)

                current_depth += 1
                offset += len(new_items)
                # YOUR CODE HERE

    def recommend(self,
                  limit=20,
                  seed_tracks=list(),
                  seed_artists=list(),
                  seed_genres=list()):
        """Given seed items, gets at most max_depth * limit
        tracks recommended by Spotify. Also, handle bad requests
        and rate limiting.
        """
        # Todo: Task 3
        # YOUR CODE HERE
        pass

    def get_new_token(self, client_id: str, client_secret: str):
        """Returns the access token gained through the client credential flow.

        If the authorization request is not accepted, raises an HTTP Error
        """
        credential_bytes = ('{}:{}'
                            .format(client_id, client_secret)
                            .encode('ascii'))
        base64_encoded = base64.b64encode(credential_bytes).decode('ascii')

        headers = {'Authorization': 'Basic {}'.format(base64_encoded)}
        payload = {'grant_type': 'client_credentials'}

        r = requests.post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=payload,
        )
        # Check that the request was successful
        r.raise_for_status()
        return r.json()['access_token']

    def save_items(self, file_path="data/spotify.json"):
        """Loads the items you've collected to a JSON file, and empties
        self.items.
        """
        import json

        with open(file_path, 'w') as outfile:
            json.dump(self.items, outfile)
            self.items = []


##############
# TEST CASES #
##############
def test_get_token():
    crawler = SpotifyCrawler('fd8abe6759d345499f8677c6c0adad96',
                             'f9f503de52fd419388387a5e82acb354')
    assert isinstance(crawler.access_token, str)


def test_search_tracks():
    crawler = SpotifyCrawler('fd8abe6759d345499f8677c6c0adad96',
                             'f9f503de52fd419388387a5e82acb354',
                             max_depth=2)
    crawler.search('kanye')

    assert isinstance(crawler.items, list)
    assert isinstance(crawler.items[0], dict)
    assert crawler.items[0]['id'] == '5brMyscUnQg14hMriS91ks'


def test_search_artists():
    crawler = SpotifyCrawler('fd8abe6759d345499f8677c6c0adad96',
                             'f9f503de52fd419388387a5e82acb354',
                             max_depth=2)
    crawler.search('kanye', item_type='artists')
    assert crawler.items[0]['id'] != '5brMyscUnQg14hMriS91ks'

def test_recommend():
    crawler = SpotifyCrawler('fd8abe6759d345499f8677c6c0adad96',
                             'f9f503de52fd419388387a5e82acb354',
                             max_depth=5)
    crawler.recommend(seed_tracks=['5brMyscUnQg14hMriS91ks'])

    assert len(crawler.items) <= crawler.max_depth * 20
    assert 'id' in crawler.items[0]
    # The following test should always raise an error
    # Spotify recommends different songs to us every time
    # Comment it out so your test works
    assert crawler.items[0]['id'] == '7aCZfs36tXkWVFItKHNGcE'


if __name__ == '__main__':
    # Todo: Task 4
    # YOUR CODE HERE
    pass
