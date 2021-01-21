import logging 
import time
import os
from flask import Flask, render_template, request, current_app, redirect, url_for
from flask_caching import Cache
#logging formatting
log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) >>> %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')

##app imports
from myproject.api_news.google_news_api import GoogleNews
from myproject.mail_manager.send_mail import EmailSender
from myproject.text2speech.get_voice_from_text import Parrot
from myproject.word_cloud.wordcloud_generator import WordCloudGenerator

#environment variables
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
os.environ['PROJECT_PATH'] = PROJECT_PATH
ARTIFACTS_PATH = os.path.join(PROJECT_PATH.replace('src', ''), 'artifacts')
os.environ['ARTIFACTS_PATH'] = ARTIFACTS_PATH

app = Flask(__name__, instance_relative_config=True)

cache = Cache()
app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)
#app.config.from_object('config')
# app.config.from_pyfile('config.py')
# print(app.config['GOOGLE_API_KEY'])
# print(app.config['EMAIL_FROM_PASSWORD'])
#print(app.config)
# TODO : Set Configuration

@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
#@cache.cached()
def home():
    if request.method == 'POST':
        company_name = request.form['company_name']
        logger.info(company_name)

        news_link, keyword = get_google_news(company_name)
        if not news_link:
            return render_template('empty_search.html', name=company_name)

        return redirect(url_for('news'))
    else:
        return render_template('home.html', title='HOME')

#cache the result
@cache.memoize()
def get_google_news(company_name):
    google = GoogleNews()
    news_link, keyword = google.get_news(keyword=company_name, num_links=8)
    cache.set('news_link', news_link)
    cache.set('keyword', keyword)
    return news_link, keyword

@app.route('/news')
def news():
    #get results from cache
    company_name = cache.get('keyword')
    news_link = cache.get('news_link')
    print(news_link)
    if not news_link: 
        template_args = {}
        return render_template('news.html', **template_args)
    news_link = [news_link[n:n+4] for n in range(0, len(news_link), 4)]
    template_args = dict(name=company_name, news_link=news_link)
    return render_template('news.html', **template_args)

@app.route('/word_cloud', methods=['GET', 'POST'])
def word_cloud():
    if request.method == 'POST':
        #get cache data
        company_name = cache.get('keyword')
        news_link = cache.get('news_link')


    return render_template('word_cloud.html', title='Word Cloud')

@app.route('/podcast', methods=['GET', 'POST'])
def podcast():
    if request.method == 'POST':
        start_time = time.time()
        #get results from cache
        company_name = cache.get('keyword')
        news_link = cache.get('news_link')
        #instanciate Parrot Class
        parrot = Parrot()
        parrot.generate_audio(news_link=news_link, keyword=company_name)
        logger.info("Audio generated")
        logger.info(f"Main program finished successfully in {round(time.time() - start_time, 4)} seconds")
    return render_template('podcast.html', title='Podcast')

@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        start_time = time.time()
        email = request.form['email']
        logger.info(f"Email To: {email}")
        send_mail = True
        if email == '' or '@' not in email:
            logger.warning(f"Email address not valid, email will not be sent.")
            send_mail = False

        #get results from cache
        company_name = cache.get('keyword')
        news_link = cache.get('news_link')

        # send mail
        if send_mail:
            mail = EmailSender(keyword=company_name, email_to=email)
            if mail.send_email_with_news(news_link_info=news_link):
                logger.info(f"Main program finished successfully in {round(time.time() - start_time, 4)} seconds")
            else:
                logger.info("Error sending the email")
    return render_template('email.html', title='Email')


if __name__ == '__main__':
    app.run(debug=True)




