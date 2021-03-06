import requests, config, base64

class Hue():
	def __init__(self):
		self.BASE_API = "https://api.meethue.com"
		self.BRIDGE_API = f"{self.BASE_API}/bridge"
		self.OAUTH_API = f"{self.BASE_API}/oauth2"

	def _convertCode(self, code: str):
		hue = config.getConfig("hue")

		url = f"{self.OAUTH_API}/token"
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

	def _getBridgeToken(self, token: str): # Gives Hue bridge token from acces token (get from getToken())
		hue = config.getConfig("hue")

		headers = {
			'authorization': f"Bearer {token}",
			'content-type': "application/json"
		}

		payload = {
			"linkbutton": True
		}
	
		requests.request("PUT", f"{self.BRIDGE_API}/0/config", json=payload, headers=headers)

		# Second Half
		payload = {
			"devicetype": hue['appid']
		}

		response = requests.request("POST", self.BRIDGE_API, json=payload, headers=headers)
		
		return response.json()[0]["success"]["username"]

	def authURL(self):
		hue = config.getConfig("hue")
		return f"{self.OAUTH_API}/auth?clientid={hue['clientid']}&appid={hue['appid']}&deviceid={hue['appid']}&state={hue['state']}&response_type=code"

	def codeToBridge(self, code: str):
		try:
			access_token = self._convertCode(code)['access_token']
		except KeyError:
			return 1 # Invalid token
		try:
			username = self._getBridgeToken(access_token)
		except KeyError:
			return 0 # Unknown Error
		return [username, access_token]
	
	def getData(self, id: int):
		url = f"{self.BRIDGE_API}/{config.getUser(id)[3]}/lights"
		accesstoken = config.getUser(id)[4]

		if accesstoken == "":
			return False

		headers = {'authorization': f'Bearer {accesstoken}'}

		try:
			r = requests.request("GET", url, headers=headers)
		except ConnectionError:
			return False

		data = r.json()

		try:
			data[0]['error']
			return "error"
		except KeyError:
			pass

		return data

if __name__ == "__main__":
	h = Hue()
	data = h.getData(0)
	for light in data:
		light = data[light]
		print(light['name'])
		print(light['state']['on'])
		print("---------\n")