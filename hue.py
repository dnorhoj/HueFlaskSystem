import requests, config

BASE_API = "https://api.meethue.com",
BRIDGE_API = f"{BASE_API}/bridge",
OAUTH_API = f"{BASE_API}/oauth2"

def generateOAuthURL():
    return "{base}/auth?clientid={clientid}&appid={appid}&deviceid={deviceid}&state={state}&response_type=code".format()

def authflow():
    pass