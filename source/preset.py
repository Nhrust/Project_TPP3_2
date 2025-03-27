from flask import *
from .sql import *
from .logic import *

DEBUG = True

app = Flask(__name__, template_folder='../templates', static_folder='../static')

base = Base("base")
# base._drop_all_tables()

accounts = AccountsManager(base)
products = ProductManager(base)
clients = ClientManager()

def get_account() -> Account:
	ip = request.remote_addr
	return clients[ip]