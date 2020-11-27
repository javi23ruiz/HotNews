import logging 
import os
from flask import Flask, render_template, request

#app imports
##app imports
from api_news.google_news_api import GoogleNews
from mail_manager.send_mail import EmailSender
from text2speech.get_voice_from_text import Parrot

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def my_email_post():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        company_name = request.form['company_name']
        print(company_name)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)