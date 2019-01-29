import requests
from bs4 import BeautifulSoup
import pandas as pd


class DataCrawler(object):
    # Example function crawling Wikipedia page for Toronto postal codes
    def get_postalcodes_data(self, url_list, columns):
        """ Crawls the list of Wikipedia URLs using BeautifulSoup
            Parses and extracts the postal codes from Toronto
            Creates a multidimensional list out of the data

        Args:
            url_list (list): List of URLs to be crawled
            columns (list): List of the column names
        Returns:
            postalcodes_df (DataFrame): Returns the data in a pandas DataFrame
        """

        postalcodes_data_list = []

        # Crawling every URL
        for url in url_list:
            r = requests.get(url)
            html = BeautifulSoup(r.text, 'lxml')

            postalcodes_table = html.find('table', {'class': 'wikitable sortable'})

            postalcodes_data_list = []
            for row in postalcodes_table.findAll('tr'):
                row_data = []
                for r in row.findAll('td'):
                    row_data.append(r.get_text().replace('\n', ''))
                if len(row_data) != 0:
                    postalcodes_data_list.append(row_data)
        # Creating DataFrame
        postalcodes_df = pd.DataFrame(postalcodes_data_list, columns=columns)
        return postalcodes_df
