import os 
import logging

##app imports
from api_news.google_news_api import GoogleNews
from mail_manager.send_mail import EmailSender

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
    logger.info('Dummy execution')

    # get news
    google = GoogleNews()
    news_link, keyword = google.get_news()

    # send mail
    mail = EmailSender(keyword=keyword)
    if mail.send_email_with_news(news_link_info=news_link):
        logger.info(f"Execeution finished successfully")
    else:
        logger.info(f"Error sending the email")

    pass

