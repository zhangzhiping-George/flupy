class HuntedBus:
    #def __init__(self, passengers=[]):
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else: 
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = HuntedBus(['s1', 's2'])

bus2 = HuntedBus()
bus2.pick('s3')

bus3 = HuntedBus()
bus3.pick('s4')

print(bus1.passengers)
print(bus2.passengers)
print(bus3.passengers)

