import utils
import database  

class User:
	def __init__(self):
		self.tools = utils.Utils()
		self.db = None  # Will be initialized with username later
		self.current_user = None
		self.tools.isConfirm = False	
	def register(self, startupPageCallback, homeCallback):
		self.tools.cls()
		print("--- Register ---")
		
		# Get user details
		firstname = str(input("First Name: "))
		self.tools.confirm(firstname)
		self.tools.isConfirm = False	
		self.tools.cls()
		lastname = str(input("Last Name: "))
		self.tools.confirm(lastname)
		self.tools.isConfirm = False	
		self.tools.cls()
		username = str(input("Username: ")).lower()
		self.tools.confirm(username)
		self.tools.isConfirm = False	
		
		# Validate PIN
		pin = ""
		while len(pin) != 4 or not pin.isdigit():
			pin = str(input("4-digit PIN: "))
			if len(pin) != 4 or not pin.isdigit():
				print("PIN must be exactly 4 digits!")
		
		confirm_pin = str(input("Confirm PIN: "))
		if pin != confirm_pin:
			print("PINs do not match!")
			input("Press ENTER to try again...")
			startupPageCallback()
			return
		
		# Encrypt PIN
		try:
			encrypted_pin = self.tools.encrypt(pin)
		except ValueError as e:
			print(f"Error: {e}")
			input("Press ENTER to try again...")
			startupPageCallback()
			return
		
		# Create user using database class
		temp_db = database.Database()  # For user operations
		
		# Check if user already exists
		if temp_db.user_exists(username):
			print(f"Username '{username}' is already taken.")
			input("Press ENTER to try again...")
			startupPageCallback()
			return
		
		# Create new user
		if temp_db.create_user(username, encrypted_pin):
			print(f"User '{username}' registered successfully!")
			
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
			
			print(f"Welcome {firstname} {lastname}!")
			input("Press ENTER to login with your new account...")
			
			self.tools.cls()
			# Login with new account
			self.current_user = username
			self.db = user_db
			homeCallback()
		else:
			print("Registration failed. Please try again.")
			input("Press ENTER to continue...")
			startupPageCallback()
	def login(self, startupPageCallback, homeCallback):
		self.tools.cls()
		print("--- Login ---")
		
		username = str(input("Username: ")).lower()
		pin = str(input("4-digit PIN: "))
		
		# Validate PIN
		if len(pin) != 4 or not pin.isdigit():
			print("Invalid PIN. PIN must be 4 digits.")
			input("Press ENTER to try again...")
			startupPageCallback()
			return
		
		# Encrypt PIN for verification
		try:
			encrypted_pin = self.tools.encrypt(pin)
		except ValueError as e:
			print(f"Error: {e}")
			input("Press ENTER to try again...")
			startupPageCallback()
			return
		
		# Verify user credentials
		temp_db = database.Database()  # For user verification
		
		if temp_db.verify_user(username, encrypted_pin):
			print(f"Login successful! Welcome {username}")
			
			# Initialize database for this user
			self.db = database.Database(username=username)
			self.current_user = username
			
			# Get user info from their budget database
			try:
				sql = "SELECT firstname, lastname FROM user_info ORDER BY id DESC LIMIT 1"
				result = self.db.query(sql)
				if result:
					firstname, lastname = result[0]
					print(f"Welcome back {firstname} {lastname}!")
			except:
				print(f"Welcome back {username}!")
			
			input("Press ENTER to continue...")
			self.tools.cls()
			homeCallback()
		else:
			print("Login failed! Username or PIN incorrect.")
			input("Press ENTER to try again...")
			self.tools.cls()
			startupPageCallback()
	def logout(self):
		"""Log out current user"""
		self.current_user = None
		self.db = None
		print("Logged out successfully.")
		return True
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