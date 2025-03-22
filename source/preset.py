from flask import *
from .sql import *

app = Flask(__name__, template_folder='../templates', static_folder="static")

base = Base("base")
