from .preset import *

@app.route("/")
def start():
	return render_template("start.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/signin")
def sigin():
	return render_template("signin.html")

@app.route("/home")
def home():
	account = get_account()
	if account == None:
		return redirect("/login",code=302)
	return render_template("home.html", products = products.get_all())

@app.route("/admin")
def admin():
	account = get_account()
	if account == None:
		return redirect("/login",code=302)
	if account.login != "admin":
		return redirect("/home",code=302)
	return render_template("admin.html", products = products.get_all())
#http://192.168.62.169:5000/add_product?name=%D0%9E%D0%B3%D1%83%D1%80%D0%B5%D1%86&price=4&category=%D0%9E%D0%B2%D0%BE%D1%89%D1%8C&picture=..%2Fstatic%2Fpictures%2Fcucumber.png