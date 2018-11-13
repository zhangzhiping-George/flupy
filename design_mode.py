from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')
class LineItem:
    def __init__(self, product, price, quantity):
        self.product = product 
        self.price = price 
        self.quantity = quantity 
    def total(self):
        return self.price*self.quantity



class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer 
        self.cart = list(cart)
        self.promotion = promotion 
    def total(self):
        return sum([item.total() for item in self.cart])
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount
    def __repr__(self): # ?why? __repr__ does't work  as being supposed
        fmt = "<Order, Total: {:.2f}, Due: {:.2f}>"
        return fmt.format(self.total(), self.due()) 

class Promotions(ABC):
    @abstractmethod
    def discount(self):
        return 'none, for being implemented in subclass'

class LargeOrderPromo(Promotions):       
    def discount(self, order):# ?why? not self.order
        products = {item.product for item in order.cart}
        if len(products) > 10:
            return order.total() * .07
        return 0
class FidelityPromo(Promotions):        
    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0
class BulkItemPromo(Promotions):       
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity > 10:
                discount += item.total() * .1
        return discount 

long_order = [LineItem(str(prod_code), 1.0, 3) for prod_code in range(11)]
bulkitem_order = [LineItem('Apple', 10, 3),
                LineItem('Banana', 3, 15),
                LineItem('Pearl', 2, 18)]

fidelity_order = [LineItem('Apple', 10, 3),
                LineItem('Banana', 3, 5),
                LineItem('Pearl', 2, 8)]
jack = Customer('Jack', 109)
ann = Customer('Jack', 1009)
print(Order(jack, long_order, promotion=LargeOrderPromo())) # ?why LargeOrderPromo with '()'?
print(Order(ann, fidelity_order, promotion=FidelityPromo())) # ?why LargeOrderPromo with '()'?
print(Order(jack, bulkitem_order, promotion=BulkItemPromo())) # ?why LargeOrderPromo with '()'?


