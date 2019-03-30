from flask import Flask, render_template, request, session, redirect, url_for
from hue import Hue
import auth, json, config

# Set up app
app = Flask(__name__)
app.secret_key = config.getConfig("secret")
PORT = 8000

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def loginsite():
	if not session.get('userID') is None:
		return redirect(url_for('controlpanel'))
	
	if request.method == 'POST':
		form = request.form.get
		
		login = auth.login(form('uname'), form('pass'))
		if login[0]:
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
		
		errorcode = auth.register(form('uname'), form('pass'), form('email'))
		login = (form('email'), form('uname'), form('pass'))
		if errorcode[0] == 0:
			session['userID'] = errorcode[1]
			return redirect(url_for('controlpanel'))
		elif errorcode[0] == 1:
			return render_template("register.html", criteria=True, login=login)
		elif errorcode[0] == 2:
			return render_template("register.html", error="Username already exists.", login=login)
		elif errorcode[0] == 3:
			return render_template("register.html", error="Email already exists.", login=login)
		elif errorcode[0] == 4:
			return render_template("register.html", error="Username is too short! It has to be at least 5 characters long", login=login)
		elif errorcode[0] == 5:
			return render_template("register.html", error="Invalid email address!", login=login)
		else:
			return "Unknown Error"

	return render_template("register.html")

@app.route('/controlpanel', methods=['GET'])
def controlpanel():
	if session.get('userID') is None:
		return redirect(url_for('index'))

	error = request.args.get('error', "0")
	h = Hue()
	return render_template(
		"controlpanel.html",
		data=h.getData(session.get("userID")),
		url=h.authURL(),
		error=error
	)

@app.route('/logout', methods=["GET"])
def logout():
	del session['userID']
	#session['userID'] = None
	return redirect(url_for('index'))

@app.route('/callback', methods=["GET"])
def callback():
	code = request.args.get('code', None)
	id = session.get('userID')

	if code is None or id is None:
		return redirect(url_for('index'))
	
	bridge = Hue().codeToBridge(code)

	if bridge == 0: # Unknown error
		return redirect(url_for('controlpanel', error=1))
	elif bridge == 1: # Invalid code
		return redirect(url_for('controlpanel', error=1))

	newdata = config.getUser(id)
	newdata[3] = bridge[0]
	newdata[4] = bridge[1]

	config.setUser(id, newdata)
	return redirect(url_for('controlpanel'))


if __name__ == '__main__':
	app.run(
		debug=True,
		host='0.0.0.0',
		port=PORT,
		#ssl_context='adhoc'
	)