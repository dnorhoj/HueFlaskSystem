from flask import Flask, render_template, request, session, redirect, url_for
import auth, json, hue, config

# Set up app
app = Flask(__name__)
app.secret_key = config.getConfig("secret")
PORT = 8000

@app.route('/')
def index():
	print(f"tis: {session}")
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def loginsite():
	if not session.get('userID') is None:
		return redirect(url_for('controlpanel'))
	
	if request.method == 'POST':
		form = request.form.get
		
		login = auth.login(form('uname'), form('pass'))
		if login[0]:
			print(login)
			session['userID'] = login[1]
			return redirect(url_for('controlpanel'))
		
		return render_template("login.html", error="Wrong password!")

	return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def registersite():
	if not session.get('userID') is None:
		return redirect(url_for('controlpanel'))

	if request.method == 'POST':
		form = request.form.get
		
		code = auth.register(form('uname'), form('pass'), form('email'))
		login = (form('email'), form('uname'), form('pass'))
		if code == 0:
			session['username'] = form('uname')
			return redirect(url_for('controlpanel'))
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
	if session.get('userID') is None:
		return redirect(url_for('index'))

	return render_template("controlpanel.html", user=config.getUsers()[session.get("userID")], url=hue.Hue().authURL())

@app.route('/logout')
def logout():
	del session['userID']
	#session['userID'] = None
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(
		debug=True,
		host='0.0.0.0',
		port=PORT,
		#ssl_context='adhoc'
	)