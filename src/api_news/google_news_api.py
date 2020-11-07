import os
import logging

from utils import load_json

log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')


class GoogleNews:
    def __init__(self):
        self.api_key = load_json(os.path.join(os.getenv('ARTIFACTS_PATH'))['google_news']['API_KEY']
        #self.brandName = brandName
        