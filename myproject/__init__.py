import os
from flask import Flask

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
print(f"basedir {basedir}")
app.config.from_pyfile('config.py')

app.config['SECRET_KEY'] = 'mysecretkey' # for the forms
