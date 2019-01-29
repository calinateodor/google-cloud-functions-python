### Introduction
This is a proof of concept function that crawls Wikipedia\'s website for Toronto postal codes, creates a pandas DataFrame out of the parsed results and uplaods the df to BQ

### How to use
* Create a `get_WEBSITE_data` method in the `DataCrawler` class where the parsing is set to be store specific
* Create a new function `load_WEBSITE_data` in `main.py` 
* Deploy a separate google cloud function that runs the specific website crawling function
   