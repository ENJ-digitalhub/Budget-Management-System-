import budget.utils as utils
import budget.database as database  
import getpass

class User:
	def __init__(self):
		self.tools = utils.Utils()
		self.db = None  # Will be initialized with username later
		self.current_user = None
						
	def register(self):
		self.tools.cls()
		# Get user details
		is_confirm = False
		while not is_confirm:
			firstname = str(input("First Name: "))
			confirm = self.tools.confirm(firstname)
			if confirm[0]:
				print(confirm[1])
				is_confirm = confirm[0]

		is_confirm = False
		while not is_confirm:
			lastname = str(input("Last Name: "))
			confirm = self.tools.confirm(lastname)
			if confirm[0]:
				print(confirm[1])
				is_confirm = confirm[0]

		is_confirm = False
		while not is_confirm:
			username = str(input("Username: ")).lower()
			confirm = self.tools.confirm(username)
			if confirm[0]:
				print(confirm[1])
				is_confirm = confirm[0]

		is_confirm = False
		while not is_confirm:
			# Validate PIN
			pin = ""
			while len(pin) != 4 or not pin.isdigit():
				pin = getpass.getpass("Set 4-digit PIN: ")
				if len(pin) != 4 or not pin.isdigit():
					print ("PIN must be exactly 4 digits!")
			
			confirm_pin = getpass.getpass("Confirm PIN: ")
			if pin != confirm_pin:
				print ("PINs do not match!")
			else:
				is_confirm = True
		
		# Encrypt PIN
		try:
			encrypted_pin = self.tools.encrypt(pin)
		except ValueError as e:
			return [False, f"Error: {e}"]
		
		# Create user using database class
		temp_db = database.Database()  # For user operations
		
		# Check if user already exists
		if temp_db.user_exists(username):
			return [False, f"Username '{username}' is already taken."]
		
		# Create new user
		if temp_db.create_user(username, encrypted_pin):
			# Create user_info table in user's budget db to store additional info
			user_db = database.Database(username=username)
			
			# Store additional user info in their budget database
			sql = """
			CREATE TABLE IF NOT EXISTS user_info (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				firstname TEXT NOT NULL,
				lastname TEXT NOT NULL,
				created_at DATETIME DEFAULT CURRENT_TIMESTAMP
			);
			"""
			user_db.run(sql)
			
			# Insert user details
			sql = "INSERT INTO user_info (firstname, lastname) VALUES (?, ?)"
			user_db.run(sql, (firstname, lastname))
			
			# Login with new account
			self.current_user = username
			self.db = user_db
			self.tools.cls()

			return [True, f"User '{username}' registered successfully!"]
			
		else:
			return [False, "Registration failed. Please try again."]

	def login(self):
		self.tools.cls()
		username = str(input("Username: ")).lower()
		pin = getpass.getpass("4-digit PIN: ")
		
		# Validate PIN
		if len(pin) != 4 or not pin.isdigit():
			return [False, "Invalid PIN. PIN must be 4 digits."]
		
		# Encrypt PIN for verification
		try:
			encrypted_pin = self.tools.encrypt(pin)
		except ValueError as e:
			return [False, f"Error: {e}"]
		
		# Verify user credentials
		temp_db = database.Database()  # For user verification
		
		if temp_db.verify_user(username, encrypted_pin):
			# Initialize database for this user
			self.db = database.Database(username=username)
			self.current_user = username
			
			# Get user info from their budget database
			try:
				sql = "SELECT firstname, lastname FROM user_info ORDER BY id DESC LIMIT 1"
				result = self.db.query(sql)
				if result:
					firstname, lastname = result[0]
					return [True, f"Login successful! Welcome back {firstname} {lastname}!"]
			except:
				return [True, f"Login successful! Welcome back {username}!"]
		else:
			return [False, "Login failed! Username or PIN incorrect."]

	def logout(self):
		"""Log out current user"""
		self.current_user = None
		self.db = None
		return [True, "Logged out successfully."]

	def get_current_user(self):
		"""Get current logged in user"""
		return self.current_user

	def get_user_db(self):
		"""Get database instance for current user"""
		return self.db

	def get_user_info(self):
		"""Get user's first and last name"""
		if not self.db or not self.current_user:
			return None
		
		try:
			sql = "SELECT firstname, lastname FROM user_info ORDER BY id DESC LIMIT 1"
			result = self.db.query(sql)
			if result:
				return result[0]
		except:
			pass
		return None