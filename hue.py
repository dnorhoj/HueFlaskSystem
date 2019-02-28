import requests, config, base64

BASE_API = "https://api.meethue.com"
BRIDGE_API = f"{BASE_API}/bridge"
OAUTH_API = f"{BASE_API}/oauth2"

def generateAuthURL():
	hue = config.getConfig("hue")
	return f"{OAUTH_API}/auth?clientid={hue['clientid']}&appid={hue['appid']}&deviceid={hue['appid']}&state={hue['state']}&response_type=code"

def getToken(code):
	hue = config.getConfig("hue")

	url = f"{OAUTH_API}/token"
	authstring = f"{hue['clientid']}:{hue['clientsecret']}"
	authstring = base64.b64encode(authstring.encode()).decode()

	querystring = {
		"code":code, 
		"grant_type":"authorization_code"
	}
	
	headers = {
		'authorization': f'Basic {authstring}'
	}

	response = requests.request("POST", url, headers=headers, params=querystring)
	
	return response.json()