class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')
        

item = LineItem('Apple', 0.8, 6)

print(item.weight)
print(item.price)
print('total: {:.2f}'.format(item.subtotal()))
item.weight = .6
print('total: {:.2f}'.format(item.subtotal()))
item.weight = -0.6

