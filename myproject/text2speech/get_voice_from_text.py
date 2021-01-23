import os 
import logging
import time
import gtts

from gtts import gTTSError
from datetime import datetime
from num2words import num2words
from playsound import playsound

#logging formatting
log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')

class Parrot:
    """Class to convert the summary of the news to a podcast
        using gTTS (it wraps the Google API for text to speech). """
    def __init__(self, language='en'):
        self.language = language

    def generate_audio(self, news_link, keyword):

        try: 
        #first concatenate all the text in one string to generate the podcast.
            start_time = time.time()
            
            today = datetime.today()
            day, week_day, month, year = today.strftime("%d"), today.strftime("%A"), \
                                        today.strftime("%B"), today.strftime("%Y")

            podcast_text = f"Hello dear user. How are you today? \
                                Welcome to the daily podcast for {keyword}. \
                                Today´s is  {week_day} the {day}th of {month} of {year}. \
                                Today´s news are: "

            for num, news in enumerate(news_link):
                news_text = f"The {num2words(num + 1, to='ordinal_num')} article is: \
                                        {news['title']}. The summary of this article \
                                        from the source {news['source']['name']} is the following. "
                podcast_text += news_text + str(news['description'] or '')
            # make request to google 
            podcast = gtts.gTTS(podcast_text, lang=self.language)

            download_folder = os.path.join(os.getenv('PROJECT_PATH').replace('src', ''), 'static/audio')
            save_name = "_".join([keyword, day, month, year])
            download_name = os.path.join(download_folder, f"{save_name}.mp3")
            podcast.save(download_name)
            logger.info(f"Podcast generated and saved in {round(time.time() - start_time, 4)} seconds")
            #playsound("hello.mp3")
            return True, f"{save_name}.mp3"

        except gTTSError as e:
            logger.info(f"Error generating the audio in the Parrot class: {e}")
            # TODO: display gtts.tts.gTTSError: 502 (Bad Gateway) from TTS API. 
            # Probable cause: Uptream API error. Try again later. If this error occurrs
            return False, ''
    
        


if __name__ == '__main__':
    audio = Parrot()
    audio.generate_audio()