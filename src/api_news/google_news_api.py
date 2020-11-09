import os
import logging
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from .utils import load_json

log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')


class GoogleNews:
    def __init__(self):
        self.api_key = load_json(os.path.join(os.getenv('ARTIFACTS_PATH'), 'credentials.json'))['google_news']['API_KEY']
        self.api_key = '6a436945bdd84b23a35b0cd91f18797d'
        
    def check_date_formats(self, from_date, to_date):
        date_format = "%Y-%m-%d"
        try:
            datetime.strptime(from_date, date_format)
            datetime.strptime(to_date, date_format)
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    def get_news(self, num_links=10, keyword="apple", sort_by='popularity',
                from_date='2020-10-10', to_date='2020-11-07'):
        

        #check dates format
        self.check_date_formats(from_date=from_date, to_date=to_date)

        url = f"https://newsapi.org/v2/everything?q={keyword}&from={from_date}&to={to_date}&sortBy={sort_by}&apiKey={self.api_key}"
        logging.info(url)
        result = requests.get(url)
        #check status of the response 
        response_status = {200:'News API request sucessfully executed', 400:'Error: Bad request parameters',
                            401:'Unauthorized request', 429:'You have reached maximun requests. Back off for a while',
                            500:'Server error in the request'}

        status_message = response_status[result.status_code]
        logging.info(f"Status News API request: {status_message}")
        if result.json()['status'] != 'ok':
            raise Exception('Error in the request of News APi. No articles returned')

        logging.info(f"Results found for News API: {result.json()['totalResults']}")
        #filter results
        news_link = result.json()['articles'][0:num_links]
        
        # keep title, description, url, urlToImage, publishAt, content
        ## TODO Change structure of this for loop
        for link in news_link:
            link.pop('source')
            link.pop('author')

        #get the text for all the parragraphs. Tag p.
        for link in news_link:
            link_result = requests.get(link['url'])
            logging.info(F"Obtaining text of the article for: {link['url']}")
            soup = BeautifulSoup(link_result.text, "lxml")
            tags_paragraph = soup.find_all('p') 
            link['content'] = " ".join(paragraph.text for paragraph in tags_paragraph)
        
        logging.info(f"OK!")

        return True



if __name__ == "__main__":
    print('yeahhh!')
    # json_path = os.path.join(os.getenv('ARTIFACTS_PATH'), 'credentials.json')
    # print(json_path)
    google = GoogleNews()
    self = google
    google.get_news()
