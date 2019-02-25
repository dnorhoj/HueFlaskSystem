import json, os

CONFIG_FILE = "json/config.json"
USER_FILE = "json/users.json"

# This checks if the user file exists, and if it doesn't it creates it.
if not os.path.exists(USER_FILE):
	open(USER_FILE, "w+").write("[]")

# Functions
def getConfig(key):
	with open(CONFIG_FILE) as f:
		data = json.load(f)
		return data[key]

def setConfig(key, value):
	with open(CONFIG_FILE) as f:
		newdata = json.load(f)
		print(newdata)
		newdata[key] = value
		with open(CONFIG_FILE, "w") as outfile:
			json.dump(newdata, outfile, indent=4)			

def getUsers():
	with open(USER_FILE) as f:
		return json.load(f)

def setUsers(json):
	with open(USER_FILE, "w") as f:
		f.write(json)