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
  
  def get_sorted_products(self, by = "price", order="Ascending"):
    products = self.get_all_products()
    reverse = (order=="Descending")
    if by == "price":
      return sorted(products, key = lambda p: p.price, reverse=reverse)
    if by == 'quantity':
      return sorted(products, key = lambda p: p.quantity, reverse=reverse)
    if by == 'expiry':
      return sorted(products, key = lambda p: p.expiry_date, reverse=reverse)
    
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
  
  def get_product_by_name(self, name):
    query = "select * from product where name=?"
    rows = self.db.execute(query, (name,), True)
    if not rows:
      return None
    return Product(*rows[0])
  
  def delete_product(self, name):
    self.db.execute("delete from product where name=?", (name,))

  def update_products(self, name, delta, category=None, price=None, expiry_date=None):
    product = self.get_product_by_name(name)

    if not product:
      if delta<=0:
        raise ValueError("cannot remove quqntity from non-existing product!!")
      if delta>0:
        if not all([price, expiry_date, category]):
          raise ValueError("New product requires category, price and expiry date")
        self.add_product(name, category, price, delta, expiry_date)
        return "product added"
    
    new_quantity = product.quantity + delta

    if new_quantity<0:
      raise ValueError("Insufficient Stock!!")
    
    elif new_quantity==0:
      self.delete_product(name)
      return "Product deleted (quantity reached zero)"
    
    else:
      self.db.execute("update product set quantity=? where name=?", (new_quantity, name))
    
    return "Quantity Updated"
  
  def unnecessary_function(self):
    return "Hello World!!"