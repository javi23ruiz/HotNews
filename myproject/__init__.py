import os
import sys
from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = 'mysecretkey' # for the forms
