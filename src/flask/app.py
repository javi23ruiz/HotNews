import logging 

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/company', methods=['POST'])
def my_email_post():
    if request.method == 'POST':
        company_name = request.form['company_name']
        print(company_name)
        email = request.form['email']
        print(email)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)