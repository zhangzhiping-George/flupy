import model7 as model 

class LineItem(model.Entity):
    desc = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, desc, weight, price):
        self.desc = desc
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

truffle = LineItem('White truffle', 100, 1)
print(truffle.weight)
print(getattr(truffle, '_Quantity#weight'))
print(LineItem.weight)
print(truffle.price)
