from .logic import *
from .pages import *

@app.route("/auth", methods = ['POST'])
def auth():
	login = request.form['login']
	password = request.form['password']
	account = accounts.try_to_login(login, password)
	
	if isinstance(account, Account):
		clients.add(request.remote_addr, account)
		resp = make_response(redirect("/home",code=302))
		resp.set_cookie("last_login", '', expires=0)
		resp.set_cookie("login_log", '', expires=0)
		return resp
	
	elif account == UI_texts.UserNotFind:
		resp = make_response(redirect("/login",code=302))
		resp.set_cookie("last_login", "")
		resp.set_cookie("login_log", account)
		return resp
	
	elif account == UI_texts.WrongPass:
		resp = make_response(redirect("/login",code=302))
		resp.set_cookie("last_login", login)
		resp.set_cookie("login_log", account)
		return resp
	
	debug_object.error("Unexpected error in /auth request")
	return redirect("/",code=302)

@app.route("/new_auth", methods=['POST'])
def new_auth():
	login = request.form['login']
	password1 = request.form['password1']
	password2 = request.form['password2']
	
	log = []
	
	if len(login) < 4:
		log.append("Login minimum length is 4")
	elif accounts.check_login(login):
		log.append("Login already exist")
	
	if password1 != password2:
		log.append("Passwords not math")
	elif len(password1) < 4:
		log.append("Password minimum length is 4")
	
	if len(log) != 0:
		resp = make_response(redirect("/signin",code=302))
		resp.set_cookie("last_signin", login)
		resp.set_cookie("signin_log", str(log))
		return resp
	
	account = accounts.add(login, password1)
	clients.add(request.remote_addr, account)

	resp = make_response(redirect("/home",code=302))
	resp.set_cookie("last_signin", '', expires=0)
	resp.set_cookie("signin_log", '', expires=0)
	return resp
	
@app.route("/logout")
def logout():
	ip = request.remote_addr
	clients.remove(ip)
	return redirect("/")
