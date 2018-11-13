def quantity():
    try:
        quantity.counter += 1
    except AttributeError:
        quantity.counter = 0
    
    storage_name = '_{}#{}'.format('quantity', quantity.counter)

    def prpty_get(instance):
        return getattr(instance, storage_name)
        
    def prpty_set(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError('value must be > 0')
    return property(prpty_get, prpty_set)

class LineItem:
    weight = quantity()
    price = quantity()

    def __init__(self, desc, weight, price):
        self.desc = desc
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
print(nutmeg.weight, nutmeg.price)
print(list(sorted(vars(nutmeg).items())))
