from datetime import datetime

class Product:

  def __init__(self, id, name, category, price, quantity, expiry_date):
      self.id = id
      self.name = name
      self.category = category
      self.price = price
      self.quantity = quantity
      self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")

  def is_expired(self, today=None):
      if not today:
        today = datetime.today()
      return self.expiry_date.date()<today.date()
         
  def can_sell(self, qty):
    return self.quantity>=qty and not self.is_expired()
  
  def sell(self, qty):
    if not self.can_Sell(qty):
      raise ValueError("cannot sell product")
    self.quantity-=qty 
    return qty*self.price
  
  def low_stock(self, threshold=5):
     return self.quantity<=threshold

  
