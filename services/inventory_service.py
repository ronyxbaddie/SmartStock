from database.db import DataBase
from models.product import Product
from datetime import datetime, timedelta

class InventoryService:
  def __init__(self):
    self.db = DataBase()
  
  def add_product(self, name, category, price, quantity, expiry_date):
      query = """
          INSERT INTO product (name, category, price, quantity, expiry_date)
          VALUES (?, ?, ?, ?, ?)
      """
      self.db.execute(query, (name, category, price, quantity, expiry_date))

  def get_all_products(self):
    rows = self.db.execute("select * from product", fetch=True)
    return [Product(*row) for row in rows]
  
  def get_sorted_products(self, by = "price"):
    products = self.get_all_products()

    if by == "price":
      return sorted(products, key = lambda p: p.price)
    if by == 'quantity':
      return sorted(products, key = lambda p: p.quantity)
    if by == 'expiry':
      return sorted(products, key = lambda p: p.expiry_date)
    
  def get_expired_products(self):
    return [p for p in self.get_all_products() if p.is_expired()]
  
  def get_low_stock_products(self, threshold=5):
    return [p for p in self.get_all_products() if p.low_stock(threshold)]
  
  def get_near_expiry_products(self, days=7):
      today = datetime.today()
      limit = today + timedelta(days=days)

      products = self.get_all_products()
      return [
          p for p in products
          if not p.is_expired() and today.date() <= p.expiry_date.date() <= limit.date()
      ]
