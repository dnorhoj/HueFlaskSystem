import requests, config, base64

class Hue():
	def __init__(self):
		self.BASE_API = "https://api.meethue.com"
		self.BRIDGE_API = f"{self.BASE_API}/bridge"
		self.OAUTH_API = f"{self.BASE_API}/oauth2"

	def _convertCode(self, code):
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

	def _getBridgeToken(self, token): # Gives Hue bridge token from acces token (get from getToken())
		hue = config.getConfig("hue")

		headers = {
			'authorization': f"Bearer {token}",
			'content-type': "application/json"
		}

		payload = {
			"linkbutton": True
		}
	
		r = requests.request("PUT", f"{self.BRIDGE_API}/0/config", json=payload, headers=headers)

		# Second Half
		payload = {
			"devicetype": hue['appid']
		}

		response = requests.request("POST", self.BRIDGE_API, json=payload, headers=headers)

		return response.text

	def authURL(self):
		hue = config.getConfig("hue")
		return f"{self.OAUTH_API}/auth?clientid={hue['clientid']}&appid={hue['appid']}&deviceid={hue['appid']}&state={hue['state']}&response_type=code"
	
	def codeToBridge(self, code):
		access_token = self._convertCode(code)['access_token']
		return self._getBridgeToken(access_token)

if __name__ == "__main__":
	h = Hue()
	print(h.codeToBridge("code"))