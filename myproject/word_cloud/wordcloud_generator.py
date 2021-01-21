import os 
import logging
import time

import wordcloud
#logging formatting
log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')

# input: list of dicts with the news
# outputs the graph


class WordCloud:
    def __init__(self):
        pass

    def generate_word_cloud(news_link_info):
        # Generate one string with the text
        pass

    def preprocess_text(raw_text):
        #remove punctuation, special characters
        # remove stopwords
        return

if __name__ == '__mian__':
    pass
