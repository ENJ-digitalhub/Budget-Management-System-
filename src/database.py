import sqlite3
import os
import time

class Database:
    # Flag to track if database is already initialized
    is_initialized = False
    @staticmethod
    def connect():
        conn = None
        max_retries = 5
        retry_delay = 1  # seconds

        # Ensure data folder exists
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print("Created data folder for database storage")

        db_path = os.path.join(data_dir, "poultry.db")

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
                conn.commit()

                # Check tables on first connection
                if not Database.is_initialized:
                    Database.check_if_tables_exist(conn)

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
    @staticmethod
    def check_if_tables_exist(conn):
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
                Database.create_all_tables(conn)
            else:
                print("Database tables are ready")

            Database.is_initialized = True

        except sqlite3.Error as e:
            print(f"Error checking for tables: {e}")
            try:
                print("Trying to create tables...")
                Database.create_all_tables(conn)
                Database.is_initialized = True
            except sqlite3.Error as e2:
                print(f"Could not create tables: {e2}")
    @staticmethod
    def init():
        conn = Database.connect()
        if conn:
            try:
                Database.create_all_tables(conn)
                Database.is_initialized = True
            except sqlite3.Error as e:
                print("Database setup failed")
                print(e)
            finally:
                conn.close()
    @staticmethod
    def create_all_tables(conn):
        cursor = conn.cursor()
        daily_records_table = """
        CREATE TABLE IF NOT EXISTS daily_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_date DATE NOT NULL UNIQUE,
            daily_allowance REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

        expenses_table = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_record_id INTEGER NOT NULL,
            label TEXT,                -- e.g. "Bus fare", "Lunch", "Netflix"
            amount REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (daily_record_id) REFERENCES daily_records(id)
        );
        """

        income_table = """
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_record_id INTEGER,
            source TEXT NOT NULL,   -- allowance top-up, profit, gift
            amount REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (daily_record_id) REFERENCES daily_records(id)
        );
        """
        
        savings_table = """
        CREATE TABLE IF NOT EXISTS savings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_record_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (daily_record_id) REFERENCES daily_records(id)
        );
        """
        
        transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,     -- debt or credit
            person TEXT,
            amount REAL NOT NULL,
            date DATE,
            settled INTEGER DEFAULT 0
        );
        """

        cursor.execute(daily_records_table)
        cursor.execute(expenses_table)
        cursor.execute(income_table)
        cursor.execute(savings_table)
        cursor.execute(transactions_table)
        conn.commit()

        print("All database tables created successfully")
    @staticmethod
    def is_database_ready():
        return Database.is_initialized
