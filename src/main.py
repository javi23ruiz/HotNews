import os 
import logging

##app imports
from api_news.google_news_api import GoogleNews

#environment variables
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
os.environ['PROJECT_PATH'] = PROJECT_PATH
ARTIFACTS_PATH = os.path.join(PROJECT_PATH.replace('src', ''), 'artifacts')
os.environ['ARTIFACTS_PATH'] = ARTIFACTS_PATH
#logging formatting
log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')

if __name__ == "__main__":
    '''Code that will be executed'''
    logger.info(os.getenv('ARTIFACTS_PATH'))
    logger.info('Dummy execution')

    google = GoogleNews()
    google.get_news()

    pass

