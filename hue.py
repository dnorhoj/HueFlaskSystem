import requests, config

BASE_API = "https://api.meethue.com"
BRIDGE_API = f"{BASE_API}/bridge"
OAUTH_API = f"{BASE_API}/oauth2"

def generateOAuthURL():
    hue = config.getConfig("hue")
    return f"{OAUTH_API}/auth?clientid={hue['clientid']}&appid={hue['appid']}&deviceid={hue['appid']}&state={hue['state']}&response_type=code"

def authflow():
    pass