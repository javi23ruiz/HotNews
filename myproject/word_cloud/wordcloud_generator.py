import os 
import logging
import time
import re
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime

#logging formatting
log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')

# input: list of dicts with the news
# outputs the graph


class WordCloudGenerator:
    def __init__(self, keyword):
        self.keyword = keyword

    def generate_word_cloud(self, news_link_info, plot=False):
        # Join all the text in one string
        full_articles_text = ''
        for link_info in news_link_info:
            full_articles_text += link_info['content']
        
        # remove punctuation, special characters
        punctuations = string.punctuation
        for character in punctuations:
            full_articles_text = full_articles_text.replace(character, '')
        
        #remove digits
        full_articles_text = re.sub(r'[0-9]+', '', full_articles_text)
        #stopwords
        stopwords = set(STOPWORDS)
        #keep lenght of words > 1
        #full_articles_text = ' '.join([w for w in full_articles_text.split() if len(w)>1])
        # Generate WordCloud
        word_cloud = WordCloud(width = 700, height = 700, 
                background_color ='black', 
                max_words=30,
                stopwords = stopwords, 
                min_font_size = 10).generate(full_articles_text) 
        logger.info("Word cloud image generated")
        ## save image 
        today = datetime.today()
        day, month, year = today.strftime("%d"), today.strftime("%B")\
                                    , today.strftime("%Y")
        save_name = "_".join([self.keyword, day, month, year]) + '.png'
        download_folder = os.path.join(os.getenv('PROJECT_PATH').replace('src', ''), 'static/images')
        word_cloud.to_file(os.path.join(download_folder, save_name))
        logger.info(f"Word cloud image sucessfully saved with the name: {save_name}")
        if plot:
            # plot the WordCloud image                        
            plt.figure(figsize = (8, 8), facecolor=None) 
            plt.imshow(word_cloud) 
            plt.axis("off") 
            plt.tight_layout(pad = 0) 
            
            plt.show() 

        return save_name


if __name__ == '__main__':
    pass
