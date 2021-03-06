import json, os

DATA_DIR = "json"
CONFIG_FILE = f"{DATA_DIR}/config.json"
USER_FILE = f"{DATA_DIR}/users.json"

# This checks if the user file exists, and if it doesn't it creates it.
if not os.path.exists(USER_FILE):
	open(USER_FILE, "w+").write("[]")

# Functions
def getConfig(key: str):
	with open(CONFIG_FILE) as f:
		data = json.load(f)
		return data[key]

def setConfig(key: str, value):
	with open(CONFIG_FILE) as f:
		newdata = json.load(f)
		newdata[key] = value
		with open(CONFIG_FILE, "w") as outfile:
			json.dump(newdata, outfile, indent=4)			

def getUsers():
	with open(USER_FILE) as f:
		return json.load(f)

def addUser(user: list):
	with open(USER_FILE) as f:
		newdata = json.load(f)
		newdata.append(user)
		with open(USER_FILE, "w") as outfile:
			json.dump(newdata, outfile, indent=4)

def getUser(id: int):
	with open(USER_FILE) as f:
		return json.load(f)[id]

def setUser(id: int, user: list):
	with open(USER_FILE) as f:
		newdata = json.load(f)
		newdata[id] = user
		with open(USER_FILE, "w") as outfile:
			json.dump(newdata, outfile, indent=4)