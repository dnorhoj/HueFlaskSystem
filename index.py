from flask import Flask, render_template, request, session, redirect
import auth, json, hue, config

# Set up app
app = Flask(__name__)
app.secret_key = config.getConfig("secret")
PORT = 8000

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def loginsite():
	if request.method == 'POST':
		form = request.form.get
		
		if auth.login(form('uname'), form('pass')):
			session['username'] = form('uname')
			return redirect("/controlpanel")
		
		return render_template("login.html", error="Wrong password!")

	return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def registersite():
	if request.method == 'POST':
		form = request.form.get
		
		code = auth.register(form('uname'), form('pass'), form('email'))
		login = (form('email'), form('uname'), form('pass'))
		if code == 0:
			session['username'] = form('uname')
			return redirect("/controlpanel")
		elif code == 1:
			return render_template("register.html", criteria=True, login=login)
		elif code == 2:
			return render_template("register.html", error="Username already exists.", login=login)
		elif code == 3:
			return render_template("register.html", error="Email already exists.", login=login)
		elif code == 4:
			return render_template("register.html", error="Username is too short! It has to be at least 5 characters long", login=login)
		elif code == 5:
			return render_template("register.html", error="Invalid email address!", login=login)
		else:
			return "Unknown Error"

	return render_template("register.html")

@app.route('/controlpanel')
def controlpanel():
	if session.get('username') is None:
		return redirect("/")

	return render_template("controlpanel.html", username=session.get("username"))
	#return session.get('username', 'Not logged in')

if __name__ == '__main__':
	app.run(
		debug=True,
		host='0.0.0.0',
		port=PORT,
		#ssl_context='adhoc'
	)