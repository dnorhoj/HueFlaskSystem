import json, hashlib, re, config

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
	users = config.getUsers()
	print(users)
	saltedpass = password+config.getConfig("salt")
	encryptedpass = hashlib.sha256(saltedpass.encode()).hexdigest()
	
	for user in range(len(users)):
		if users[user][1] == username:
			print(users[user])
			if users[user][2] == encryptedpass:
				return [True, user]

	print(f"Username: '{username}' not found")
	return [False]

# Register function
def register(username, password, email):
	if not checkpass(password):
		return [1] # 1 = Password does not meet criterias
	elif len(username) < 5:
		return [4] # 4 = Username is too short
	elif re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
		return [5] # 5 = Email is invalid
	
	users = config.getUsers()

	id = 0
	for user in users:
		if user[1] == username:
			return [2] # 2 = Username already exist
		elif user[0] == email:
			return [3] # 3 = Email already exist
		id+=1
	
	# Hash password
	saltedpass = password+config.getConfig("salt")
	encryptedpass = hashlib.sha256(saltedpass.encode()).hexdigest()
	
	user = [] # Create user object
	user.append(email) # Email field
	user.append(username) # Username field
	user.append(encryptedpass) # Encrypted password field
	user.append("") # There's no Hue API Key (yet)

	config.addUser(user) # Add user to file

	return [0, id] # 0 = Success