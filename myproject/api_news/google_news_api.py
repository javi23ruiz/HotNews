import os
import logging
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
#from .utils import load_json

from run import app

log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')


class GoogleNews:
    def __init__(self):
        #self.api_key = load_json(os.path.join(os.getenv('ARTIFACTS_PATH'), 'credentials.json'))['google_news']['API_KEY']
        self.api_key = '6a436945bdd84b23a35b0cd91f18797d'
        
    def check_date_formats(self, from_date, to_date):
        date_format = "%Y-%m-%d"
        try:
            datetime.strptime(from_date, date_format)
            datetime.strptime(to_date, date_format)
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    def get_news(self, keyword, num_links=12, sort_by='relevancy',
                from_date=(datetime.today() - timedelta(days=15)).strftime('%Y-%m-%d'), 
                to_date=datetime.today().strftime('%Y-%m-%d')):
    
        #check dates format
        self.check_date_formats(from_date=from_date, to_date=to_date)

        url = f"https://newsapi.org/v2/everything?q={keyword}&from={from_date}&to={to_date}&sortBy={sort_by}&apiKey={self.api_key}"
        logging.info(f"url for news pai: {url}")
        result = requests.get(url)
        #check status of the response 

        try: 
            response_status = {200:'News API request sucessfully executed', 400:'Error: Bad request parameters',
                                401:'Unauthorized request', 500:'Server error in the request',
                                429:'You have reached maximun requests. Back off for a while'}
            logger.info(result.status_code)
            status_message = response_status[result.status_code]
            logger.info(f"Status News API request: {status_message}")
        except Exception as e:
            logger.info(f"Unknown status code {result.status_code}")
            raise Exception('Unknown status code')

        if (result.json()['status'] != 'ok') and (result.json()['code'] == "parameterInvalid"):
            logger.info(f"Check API parameters. Can only go back in time for one month from today´s date.")
        elif result.json()['status'] != 'ok':
            logger.info(f"Error Message: {result.json()['message']}")
            raise Exception('Error in the request of News API. No articles returned')

        logging.info(f"Results found for News API: {result.json()['totalResults']}")
        #filter results
        news_link = result.json()['articles'][0:num_links]
        
        # keep title, description, url, urlToImage, publishAt, content
        ## TODO Change structure of this for loop
        for link in news_link:
            link.pop('author')

        #get the text for all the parragraphs. Tag p.
        for link in news_link:
            logger.debug(f"Proccessing: {link['url']}")
            try:
                link_result = requests.get(link['url'])
                soup = BeautifulSoup(link_result.text, "lxml")
                tags_paragraph = soup.find_all('p') 
                link['content'] = " ".join(paragraph.text for paragraph in tags_paragraph)
            except Exception as e: 
                logger.info(f"Error processing the link {e}")
                link['content'] = ''
         
        logger.info(f"News API information retreived successfully!")

        return news_link, keyword



if __name__ == "__main__":
    print('yeahhh!')
    # json_path = os.path.join(os.getenv('ARTIFACTS_PATH'), 'credentials.json')
    # print(json_path)
    #empty list evaluate to False
    google = GoogleNews()
    self = google
    news_link, _ = google.get_news(keyword='CrowdAI')
    if not news_link:
        print('empty list')
    print(news_link)