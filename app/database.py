import sqlite3
import os
from datetime import datetime

DB_NAME = "biz_analytics.db"

class DatabaseManager:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Creates a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn

    def _init_db(self):
        """Initializes the database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Customers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                gender TEXT CHECK(gender IN ('Male', 'Female', 'Other', 'Unknown')) DEFAULT 'Unknown',
                contact TEXT,
                first_purchase_date DATE DEFAULT (DATE('now')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Transactions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                amount REAL NOT NULL,
                txn_type TEXT CHECK(txn_type IN ('Income', 'Expense')) NOT NULL,
                category TEXT NOT NULL,
                reason TEXT,
                payment_method TEXT NOT NULL,
                txn_date DATE DEFAULT (DATE('now')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        """)
        
        conn.commit()
        conn.close()

    def execute_query(self, query, params=()):
        """Executes a write query (INSERT, UPDATE, DELETE)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            raise
        finally:
            conn.close()

    def fetch_all(self, query, params=()):
        """Executes a read query (SELECT) and returns all results."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def fetch_one(self, query, params=()):
        """Executes a read query (SELECT) and returns one result."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

# Singleton instance for easy access
db = DatabaseManager()
