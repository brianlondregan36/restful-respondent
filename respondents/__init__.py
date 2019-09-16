from flask import Flask
app = Flask(__name__)

from .respondents import respondents.views
from .respondents import respondents.passwords
