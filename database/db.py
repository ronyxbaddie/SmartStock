import sqlite3
import os

curr_path = os.path.abspath(__file__)
back_path = os.path.dirname(os.path.dirname(curr_path))
db_path = os.path.join(back_path, "smartstock.db")

class DataBase:

  def __init__(self):
    self.conn = sqlite3.connect(db_path, check_same_thread=False)
    self.cursor = self.conn.cursor()

  def execute(self, query, params=(), fetch = False):
    self.cursor.execute(query, params)
    self.conn.commit()
    if fetch:
      return self.cursor.fetchall()
    
  def create_tables(self):
      self.cursor.execute("""
          CREATE TABLE IF NOT EXISTS product (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              category TEXT,
              price REAL,
              quantity INTEGER,
              expiry_date TEXT
          )
      """)

      self.cursor.execute("""
          CREATE TABLE IF NOT EXISTS sales (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              product_id INTEGER,
              quantity INTEGER,
              total REAL,
              sale_date TEXT
          )
      """)

      self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
      
      self.conn.commit()
    