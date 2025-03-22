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
    return render_template("home.html")

