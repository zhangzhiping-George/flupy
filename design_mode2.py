from collections import namedtuple
import inspect
import promotions

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
            discount = self.promotion(self)
        return self.total() - discount
    def __repr__(self): # ?why? __repr__ does't work  as being supposed
        fmt = "<Order, Total: {:.2f}, Due: {:.2f}>"
        return fmt.format(self.total(), self.due()) 

long_order = [LineItem(str(prod_code), 1.0, 3) for prod_code in range(11)]
bulkitem_order = [LineItem('Apple', 10, 3),
                LineItem('Banana', 3, 15),
                LineItem('Pearl', 2, 18)]

fidelity_order = [LineItem('Apple', 10, 3),
                LineItem('Banana', 3, 5),
                LineItem('Pearl', 2, 8)]
jack = Customer('Jack', 109)
ann = Customer('Jack', 1009)

#names = [name for name in globals()]
#print(names)

#promos = [globals()[name] for name in globals().keys() if name.endswith('_promo') and name != 'best_promo']
promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]
print(promos)


#promo_list = [large_order_promo, fidelity_promo, bulkitem_promo]
def best_promo(order):
    return max(promo(order) for promo in promos)


print(Order(jack, long_order, promotion=best_promo)) 
print(Order(ann, fidelity_order, promotion=best_promo)) 
print(Order(jack, bulkitem_order, promotion=best_promo))


