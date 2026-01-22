import sqlite3
import os
import time

class Database:
	def __init__(self, username=None):
		# Flag to track if database is already initialized
		self.is_initialized = False
		self.current_username = username
		
		# For backward compatibility - main connection is to user's budget db
		if username:
			conn = self.connect_to_user_db(username)
			if conn:
				try:
					self.create_all_tables(conn, username)
					self.is_initialized = True
				except sqlite3.Error as e:
					print("Database setup failed")
					print(e)
				finally:
					conn.close()
	def connect(self):
		"""Backward compatibility method - connects to current user's budget db"""
		if not self.current_username:
			print("No user logged in")
			return None
		return self.connect_to_user_db(self.current_username)
	def connect_to_user_db(self, username):
		"""Connect to a specific user's budget database"""
		conn = None
		max_retries = 5
		retry_delay = 1  # seconds

		# Get the path to the parent folder (where src/ lives)
		base_dir = os.path.dirname(os.path.abspath(__file__))  # __file__ is src/database.py
		project_dir = os.path.dirname(base_dir)   
		
		# Ensure data folder exists
		data_dir = os.path.join(project_dir, "data")
		if not os.path.exists(data_dir):
			os.makedirs(data_dir)
			print("Created data folder")
		
		# Ensure user directory exists
		user_dir = os.path.join(data_dir, username)
		if not os.path.exists(user_dir):
			os.makedirs(user_dir)
			print(f"Created directory for user: {username}")

		db_path = os.path.join(user_dir, "budget.db")

		for attempt in range(1, max_retries + 1):
			try:
				conn = sqlite3.connect(
					db_path,
					timeout=5,
					check_same_thread=False
				)

				# Set pragmas (similar to JDBC parameters)
				cursor = conn.cursor()
				cursor.execute("PRAGMA journal_mode=WAL;")
				cursor.execute("PRAGMA synchronous=NORMAL;")
				cursor.execute("PRAGMA locking_mode=NORMAL;")
				cursor.execute("PRAGMA busy_timeout=5000;")
				cursor.execute("PRAGMA foreign_keys = ON;")
				conn.commit()

				print(f"Connected to {username}'s budget database (attempt {attempt})")
				return conn

			except sqlite3.Error as e:
				print(f"Connection attempt {attempt} for {username} failed: {e}")

				if conn:
					conn.close()

				if attempt < max_retries:
					print(f"Retrying in {retry_delay} seconds...")
					time.sleep(retry_delay)
					retry_delay *= 2  # Exponential backoff
				else:
					print(f"Failed to connect after {max_retries} attempts")

		return None
	def connect_to_users_db(self):
		"""Connect to the central users database"""
		conn = None
		max_retries = 5
		retry_delay = 1  # seconds

		# Get the path to the parent folder (where src/ lives)
		base_dir = os.path.dirname(os.path.abspath(__file__))
		project_dir = os.path.dirname(base_dir)   
		
		# Ensure data folder exists
		data_dir = os.path.join(project_dir, "data")
		if not os.path.exists(data_dir):
			os.makedirs(data_dir)

		db_path = os.path.join(data_dir, "users.db")

		for attempt in range(1, max_retries + 1):
			try:
				conn = sqlite3.connect(
					db_path,
					timeout=5,
					check_same_thread=False
				)

				# Set pragmas
				cursor = conn.cursor()
				cursor.execute("PRAGMA journal_mode=WAL;")
				cursor.execute("PRAGMA synchronous=NORMAL;")
				cursor.execute("PRAGMA locking_mode=NORMAL;")
				cursor.execute("PRAGMA busy_timeout=5000;")
				conn.commit()

				print(f"Connected to users database (attempt {attempt})")
				return conn

			except sqlite3.Error as e:
				print(f"Users DB connection attempt {attempt} failed: {e}")
				if attempt < max_retries:
					time.sleep(retry_delay)
					retry_delay *= 2
				else:
					print(f"Failed to connect to users DB after {max_retries} attempts")

		return None
	def check_if_tables_exist(self, conn, username):
		"""Check if budget tables exist for a user"""
		try:
			cursor = conn.cursor()
			cursor.execute("""
				SELECT COUNT(*) 
				FROM sqlite_master 
				WHERE type='table' AND name='allowance'
			""")
			count = cursor.fetchone()[0]

			if count == 0:
				print(f"Creating budget tables for {username}...")
				self.create_all_tables(conn, username)
			else:
				print(f"Budget tables ready for {username}")

			self.is_initialized = True

		except sqlite3.Error as e:
			print(f"Error checking for tables: {e}")
			try:
				print("Trying to create tables...")
				self.create_all_tables(conn, username)
				self.is_initialized = True
			except sqlite3.Error as e2:
				print(f"Could not create tables: {e2}")
	def create_all_tables(self, conn, username=None):
		"""Create all budget tables for a user"""
		cursor = conn.cursor()
		
		allowance_table = """
		CREATE TABLE IF NOT EXISTS allowance (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			record_date DATE UNIQUE NOT NULL DEFAULT CURRENT_DATE,
			amount REAL NOT NULL,
			created_at TIME DEFAULT CURRENT_TIME
		);
		"""

		expenses_table = """
		CREATE TABLE IF NOT EXISTS expenses (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			allowance_id INTEGER,
			label TEXT DEFAULT NULL,
			amount REAL NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (allowance_id) REFERENCES allowance(id)
		);
		"""

		income_table = """
		CREATE TABLE IF NOT EXISTS income (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			allowance_id INTEGER,
			label TEXT DEFAULT NULL,
			amount REAL NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (allowance_id) REFERENCES allowance(id)
		);
		"""
		
		savings_table = """
		CREATE TABLE IF NOT EXISTS savings (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			allowance_id INTEGER,
			amount REAL NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (allowance_id) REFERENCES allowance(id)
		);
		"""
		
		cursor.execute(allowance_table)
		cursor.execute(expenses_table)
		cursor.execute(income_table)
		cursor.execute(savings_table)
		conn.commit()

		if username:
			print(f"Budget tables created successfully for {username}")
		else:
			print("Budget tables created successfully")
	def create_user_table(self):
		"""Create the central users table if it doesn't exist"""
		conn = self.connect_to_users_db()
		if not conn:
			print("Failed to connect to users database")
			return False
		
		try:
			cursor = conn.cursor()
			user_table = """
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				username TEXT UNIQUE NOT NULL,
				encrypted_pin TEXT NOT NULL,
				created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
				last_login DATETIME
			);
			"""
			cursor.execute(user_table)
			conn.commit()
			print("Users table created successfully")
			return True
		except sqlite3.Error as e:
			print(f"Error creating users table: {e}")
			return False
		finally:
			conn.close()
	def is_database_ready(self):
		return self.is_initialized
	def run(self, sql, params=None):
		"""Execute SQL on current user's budget database - MAINTAINS EXISTING INTERFACE"""
		conn = self.connect()  # Connects to current user's budget db
		if not conn:
			print("Database connection failed. Cannot execute SQL.")
			return
		
		try:
			cursor = conn.cursor()
			if params:
				cursor.execute(sql, params)
			else:
				cursor.execute(sql)
			conn.commit()
		except sqlite3.Error as e:
			print(f"Database error: {e}")
			conn.rollback()
		finally:
			conn.close()
	def query(self, sql, params=None):
		"""Query current user's budget database - MAINTAINS EXISTING INTERFACE"""
		conn = self.connect()  # Connects to current user's budget db
		if not conn:
			print("Database connection failed. Cannot execute SQL.")
			return ()
		
		try:
			cursor = conn.cursor()
			if params:
				cursor.execute(sql, params)
			else:
				cursor.execute(sql)
			rows = tuple(cursor.fetchall())
			return rows
		except sqlite3.Error as e:
			print(f"Database error: {e}")
			return ()
		finally:
			conn.close()
	# New methods for user management (to be used by user.py module)
	def user_exists(self, username):
		"""Check if a user exists in the central users database"""
		conn = self.connect_to_users_db()
		if not conn:
			return False
		
		try:
			cursor = conn.cursor()
			cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
			count = cursor.fetchone()[0]
			return count > 0
		except sqlite3.Error:
			# If users table doesn't exist yet
			return False
		finally:
			conn.close()
	def create_user(self, username, encrypted_pin):
		"""Create a new user in central database and initialize their budget db"""
		# First ensure users table exists
		self.create_user_table()
		
		conn = self.connect_to_users_db()
		if not conn:
			return False
		
		try:
			cursor = conn.cursor()
			cursor.execute(
				"INSERT INTO users (username, encrypted_pin) VALUES (?, ?)",
				(username, encrypted_pin)
			)
			conn.commit()
			
			# Now initialize user's budget database
			budget_conn = self.connect_to_user_db(username)
			if budget_conn:
				self.create_all_tables(budget_conn, username)
				budget_conn.close()
				print(f"User {username} created successfully with budget database")
				return True
			
			return False
		except sqlite3.IntegrityError:
			print(f"Username {username} already exists")
			return False
		except sqlite3.Error as e:
			print(f"Error creating user: {e}")
			return False
		finally:
			conn.close()
	def verify_user(self, username, encrypted_pin):
		"""Verify user credentials"""
		conn = self.connect_to_users_db()
		if not conn:
			return False
		
		try:
			cursor = conn.cursor()
			cursor.execute(
				"SELECT username FROM users WHERE username = ? AND encrypted_pin = ?",
				(username, encrypted_pin)
			)
			result = cursor.fetchone()
			if result:
				# Update last login
				cursor.execute(
					"UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?",
					(username,)
				)
				conn.commit()
				return True
			return False
		except sqlite3.Error as e:
			print(f"Error verifying user: {e}")
			return False
		finally:
			conn.close()