import sqlite3
import os
import time

class Database:
    def __init__(self):
        # Flag to track if database is already initialized
        self.is_initialized = False
        conn = self.connect()
        if conn:
            try:
                self.create_all_tables(conn)
                self.is_initialized = True
            except sqlite3.Error as e:
                print("Database setup failed")
                print(e)
            finally:
                conn.close()
    def connect(self):
        conn = None
        max_retries = 5
        retry_delay = 1  # seconds

        # Get the path to the parent folder (where src/ lives)
        base_dir = os.path.dirname(os.path.abspath(__file__))  # __file__ is src/database.py
        project_dir = os.path.dirname(base_dir)   
        # Ensure data folder exists
        data_dir = os.path.join(project_dir,"data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print("Created data folder for database storage")

        db_path = os.path.join(data_dir,"budget.db")

        for attempt in range(1,max_retries + 1):
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

                # Check tables on first connection
                if not self.is_initialized:
                    self.check_if_tables_exist(conn)

                print(f"Connected to database successfully (attempt {attempt})")
                return conn

            except sqlite3.Error as e:
                print(f"Connection attempt {attempt} failed: {e}")

                if conn:
                    conn.close()

                if attempt < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"Failed to connect after {max_retries} attempts")

        return None
    def check_if_tables_exist(self,conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM sqlite_master 
                WHERE type='table' AND name='users'
            """)
            count = cursor.fetchone()[0]

            if count == 0:
                print("Tables not found - creating them now...")
                self.create_all_tables(conn)
            else:
                print("Database tables are ready")

            self.is_initialized = True

        except sqlite3.Error as e:
            print(f"Error checking for tables: {e}")
            try:
                print("Trying to create tables...")
                self.create_all_tables(conn)
                self.is_initialized = True
            except sqlite3.Error as e2:
                print(f"Could not create tables: {e2}")    
    def create_all_tables(self,conn):
        cursor = conn.cursor()
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            pin TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
        
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
            label TEXT DEFAULT NULL,             -- e.g. "Bus fare","Lunch","Netflix"
            amount REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (allowance_id) REFERENCES allowance(id)
        );
        """

        income_table = """
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            allowance_id INTEGER,
            label TEXT DEFAULT NULL,-- allowance top-up,profit,gift
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
        
        transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,  -- debt or credit
            person TEXT,
            amount REAL NOT NULL,
            date DATE,
            settled INTEGER DEFAULT 0
        );
        """

        cursor.execute(users_table)
        cursor.execute(allowance_table)
        cursor.execute(expenses_table)
        cursor.execute(income_table)
        cursor.execute(savings_table)
        cursor.execute(transactions_table)
        conn.commit()

        print("All database tables created successfully")
    def is_database_ready(self):
        return self.is_initialized
    def run(self,sql,params=None):
        conn = self.connect()  # uses your robust connect() method
        if not conn:
            print("Database connection failed. Cannot execute SQL.")
            return
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql,params)
            else:
                cursor.execute(sql)
            conn.commit()
        finally:
            conn.close()
    def query(self,sql,params=None):
        conn = self.connect()  # uses your robust connect() method
        if not conn:
            print("Database connection failed. Cannot execute SQL.")
            return
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql,params)
            else:
                cursor.execute(sql)
        finally:
            rows = tuple(cursor.fetchall())
            conn.close()
            return rows