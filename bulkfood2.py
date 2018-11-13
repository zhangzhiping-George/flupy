def quantity(storage_name):

    def prpty_get(instance):
        return instance.__dict__[storage_name]

    def prpty_set(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(prpty_get, prpty_set)

class LineItem:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, desc, weight, price):
        self.desc = desc
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
print(nutmeg.weight, nutmeg.price)
print(list(sorted(vars(nutmeg).items())))
