import time
import random

import requests
from bs4 import BeautifulSoup


class BillboardCrawler:
    """BillboardCrawler recursively extracts chart data
    from www.billboard.com

    Instantiate a BillboardCrawler and run the .crawl()
    method to collect data in the attribute self.items.
    """
    base_url = 'http://www.billboard.com'

    def __init__(self,
                 start_url='http://www.billboard.com/charts/hot-100',
                 end_url=None,
                 recursion_depth=None,
                 download_delay=1):
        self.start_url = start_url
        self.end_url = end_url
        self.recursion_depth = recursion_depth
        # The number of seconds to wait between requests
        self.download_delay = download_delay
        # Where the data to be collected is stored
        self.items = []

    def parse_chart(self, response: requests.models.Response) -> None:
        """Extracts the chart data from the given HTTP response.
        Each row is a dictionary containing the following about one song:

            the week of the chart,
            the song's chart rank that week,
            the name of the songs,
            the names of the artists,

        See data/solutions/hot100.csv for examples of how the data should look.
        """
        soup = BeautifulSoup(response.text, 'html.parser')

        ### TODO: Task 8
        # YOUR CODE HERE

        # If a link to the previous week exists, crawls that link
        if soup.find(title='Previous Week'):
            next_url = self.base_url + soup.find(title='Previous Week')['href']
            return self.get_response(next_url)

    def get_response(self, url):
        """Checks a few conditions before getting the next HTTP response.
        Stops crawling if the input url equals the end url. Delays the next
        HTTP request by self.download_delay seconds.
        """
        print('Requesting data from:', url)
        if url == self.end_url:
            return

        time.sleep(random.random() * self.download_delay)
        response = requests.get(url)
        return self.parse_chart(response)

    def crawl(self):
        """Starts crawling Billboard"""
        self.get_response(self.start_url)

    def save_items(self, file_path="spotify.json"):
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
def test_end():
    start_url = 'http://www.billboard.com/charts/hot-100/2017-09-09'
    end_url = 'http://www.billboard.com/charts/hot-100/2017-09-09'
    crawler = BillboardCrawler(start_url=start_url, end_url=end_url)
    crawler.crawl()
    assert len(crawler.items) == 0


def test_crawler():
    start_url = 'http://www.billboard.com/charts/hot-100/2017-09-16'
    end_url = 'http://www.billboard.com/charts/hot-100/2017-09-09'
    crawler = BillboardCrawler(start_url=start_url, end_url=end_url)
    crawler.crawl()

    assert len(crawler.items) == 100
    assert isinstance(crawler.items[0], dict)
    assert crawler.items[0] == {'week': '2017-09-16',
                                'rank': '1',
                                'song_name': 'Look What You Made Me Do',
                                'artist_names': 'Taylor Swift'}
    assert crawler.items[99] == {'artist_names': 'Brothers Osborne',
                                 'rank': '100',

                                 'song_name': "It Ain't My Fault",

                                 'week': '2017-09-16'}


def test_recursion():
    start_url = 'http://www.billboard.com/charts/hot-100/2017-09-23'
    end_url = 'http://www.billboard.com/charts/hot-100/2017-09-09'
    crawler = BillboardCrawler(start_url=start_url, end_url=end_url)
    crawler.crawl()
    assert len(crawler.items) == 200
    assert isinstance(crawler.items[0], dict)
    assert crawler.items[0] == {'week': '2017-09-23',
                                'rank': '1',
                                'song_name': 'Look What You Made Me Do',
                                'artist_names': 'Taylor Swift'}
    assert crawler.items[99] == {'artist_names': 'DeJ Loaf',
                                 'rank': '100',
                                 'song_name': 'No Fear',
                                 'week': '2017-09-23'}

if __name__ == '__main__':
    start_url = 'http://www.billboard.com/charts/hot-100/2017-09-16'
    end_url = 'http://www.billboard.com/charts/hot-100/2015-09-12'
    crawler = BillboardCrawler(start_url=start_url, end_url=end_url)
    crawler.crawl()
    crawler.save_items('data/hot100.json')