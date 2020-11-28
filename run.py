import logging 
import time
import os
from flask import Flask, render_template, request

#logging formatting
log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')

##app imports
from app.api_news.google_news_api import GoogleNews
from app.mail_manager.send_mail import EmailSender
from app.text2speech.get_voice_from_text import Parrot

#environment variables
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
os.environ['PROJECT_PATH'] = PROJECT_PATH
ARTIFACTS_PATH = os.path.join(PROJECT_PATH.replace('src', ''), 'artifacts')
os.environ['ARTIFACTS_PATH'] = ARTIFACTS_PATH

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def my_email_post():
    if request.method == 'POST':
        start_time = time.time()
        email = request.form['email']
        logger.info(email)
        company_name = request.form['company_name']
        logger.info(company_name)

        # get news
        google = GoogleNews()
        news_link, keyword = google.get_news(keyword=company_name)
        # send mail
        mail = EmailSender(keyword=company_name, email_to=email)
        if mail.send_email_with_news(news_link_info=news_link):
            parrot = Parrot()
            parrot.generate_audio(news_link=news_link, keyword=company_name)
            logger.info("Audio generated")
            logger.info(f"Main program finished successfully in {round(time.time() - start_time, 4)} seconds")
        else:
            logger.info("Error sending the email")

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)



