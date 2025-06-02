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
		return redirect("/login", code=302)
	
	return render_template("home.html", products = products.get_all(), categories = products.get_categories())

@app.route("/admin")
def admin():
	account = get_account()
	if account == None:
		return redirect("/login",code=302)
	if account.login != "admin":
		return redirect("/home",code=302)
	return render_template("admin.html", products = products.get_all())

@app.route("/cart")
def cart():
	return render_template("cart.html")
