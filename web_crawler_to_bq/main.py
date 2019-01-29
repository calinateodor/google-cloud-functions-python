import requests
import pandas as pd
from bs4 import BeautifulSoup
from data_crawler import DataCrawler


project_name = 'PROJECT_NAME' # Add project name
dataset_name = 'DATASET_NAME' # Add a dataset name
table_name = 'TABLE_NAME' # Add a table name
destination_table = '{}.{}'.format(dataset_name, table_name)
write_disposition = 'append'

def load_postalcodes_data(request):
    """Runs the crawling function, creates dataframe and uploads it to BQ

    Args:
        request (google.cloud.functions.Request): Metadata of triggering event
    Returns:
        None; the output is written to Stackdriver Logging
    """

    #Add the links to be crawled
    url_list = ['https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'] # Add here links
    columns = ['Postcode', 'Borough', 'Neighbourhood']

    dc = DataCrawler()
    postalcodes_df = dc.get_postalcodes_data(url_list=url_list, columns=columns)
    postalcodes_df.to_gbq(destination_table=destination_table,
                          project_id=project_name,
                          chunksize=None,
                          if_exists=write_disposition
                          )
