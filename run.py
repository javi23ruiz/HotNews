import logging 
import time
import os
from flask import Flask, render_template, request, current_app

#logging formatting
log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')

##app imports
from myproject.api_news.google_news_api import GoogleNews
from myproject.mail_manager.send_mail import EmailSender
from myproject.text2speech.get_voice_from_text import Parrot

#environment variables
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
os.environ['PROJECT_PATH'] = PROJECT_PATH
ARTIFACTS_PATH = os.path.join(PROJECT_PATH.replace('src', ''), 'artifacts')
os.environ['ARTIFACTS_PATH'] = ARTIFACTS_PATH

app = Flask(__name__, instance_relative_config=True)
#app.config.from_object('config')
# app.config.from_pyfile('config.py')
# print(app.config['GOOGLE_API_KEY'])
# print(app.config['EMAIL_FROM_PASSWORD'])
#print(app.config)
# TODO : Set Configuration


#@app.route('/')
#def email():
#    return render_template('home_new.html')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def my_email_post():
    if request.method == 'POST':
        start_time = time.time()
        send_mail = True
        email = request.form['email']
        if email == '' or '@' not in email:
            logger.warning(f"Email address not valid, email will not be sent.")
            send_mail = False

        logger.info(f"Email: {email}")
        company_name = request.form['company_name']
        logger.info(company_name)

        # get news
        google = GoogleNews()
        news_link, keyword = google.get_news(keyword=company_name)
        if not news_link:
            return render_template('empty_search.html', name=company_name)

        # send mail
        if send_mail:
            mail = EmailSender(keyword=company_name, email_to=email)
            if mail.send_email_with_news(news_link_info=news_link):
                parrot = Parrot()
                parrot.generate_audio(news_link=news_link, keyword=company_name)
                logger.info("Audio generated")
                logger.info(f"Main program finished successfully in {round(time.time() - start_time, 4)} seconds")
            else:
                logger.info("Error sending the email")

        #group the news in list of list of 4 elements to display them when rendering the template
        news_link = [news_link[n:n+4] for n in range(0, len(news_link), 4)]
        template_args = dict(name=company_name, news_link=news_link)

    return render_template('news.html', **template_args)


if __name__ == '__main__':
    app.run(debug=True)




