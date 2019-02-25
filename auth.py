import json, hashlib, re

# Filenames
DATAFILE = "data.json"

# Check if password is valid
def checkpass(password):
	if re.match(r'.{7}', password) is None:
		return False
	elif re.search(r'[A-Z][a-z]|[a-z][A-Z]', password) is None:
		return False

	return True

# Login function
def login(username, password):
	with open(DATAFILE) as f:
		data = json.load(f)

		for info in data["users"]:
			if info[1] == username:

				saltedpass = password+data["salt"]
				encryptedpass = hashlib.sha256(saltedpass.encode()).hexdigest()

				if info[2] == encryptedpass:
					return True

		print(f"Username: {username} not found")
		return False

# Register function
def register(username, password, email=None):
	if not checkpass(password):
		return 1 # 1 = Password does not meet criterias
	elif len(username) < 5:
		return 4 # 4 = Username is too short
	elif re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
		return 5 # 5 = Email is invalid
		
	with open(DATAFILE) as f:
		data = json.load(f)
		for user in data["users"]:
			if user[1] == username:
				return 2 # 2 = Username already exist
			elif user[0] == email:
				return 3 # 3 = Email already exist

		user = []
		user.append(email) # Email field
		user.append(username) # Username field

		saltedpass = password+data["salt"]
		encryptedpass = hashlib.sha256(saltedpass.encode()).hexdigest()
		user.append(encryptedpass) # Encrypted password field
		user.append("") # There's no Hue API Key (yet)

		data["users"].append(user)

		with open(DATAFILE, 'w') as outfile:  
			json.dump(data, outfile, indent=4)
			return 0 # 0 = Success