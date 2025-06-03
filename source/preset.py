from flask import *
from flask_socketio import SocketIO, emit
from .sql import *
from .logic import *
from os import path

DEBUG = True

app = Flask(__name__, template_folder='../templates', static_folder='../static')
socket = SocketIO(app)

base = Base("base")
# base._drop_all_tables()

accounts = AccountsManager(base)
products = ProductManager(base)
clients = ClientManager()

def get_account() -> Account:
	ip = request.remote_addr
	return clients[ip]

@socket.on("add_to_cart")
def add_to_cart(product_id: str):
	product_id = int(product_id)
	acc = get_account()
	acc.add_to_cart(product_id)
	d = eval(acc.cart)
	nd = dict()
	for k in d:
		nd[str(k)] = d[k]
	emit("cart", str(nd).replace("'", '"'))

@socket.on("remove_from_cart")
def remove_from_cart(product_id: str):
	product_id = int(product_id)
	acc = get_account()
	acc.remove_from_cart(product_id)
	d = eval(acc.cart)
	nd = dict()
	for k in d:
		nd[str(k)] = d[k]
	emit("cart", str(nd).replace("'", '"'))

@socket.on("get_cart")
def add_to_cart():
	acc = get_account()
	d = eval(acc.cart)
	nd = dict()
	for k in d:
		nd[str(k)] = d[k]
	emit("cart", str(nd).replace("'", '"'))
