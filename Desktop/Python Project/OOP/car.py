
class Warehouse:
    def __init__(self, name):
        self.name = name
        self.inventory = []

    def add_goods(self, goods):
        self.inventory.append(goods)
    
    def describe(self):
        return [f"{goods.desc}" for goods in self.inventory]

class Drygoods:
    def __init__(self, desc, weight):
        self.desc = desc
        self.weight = weight

warehouse = Warehouse('Houston Department Warehouse')

drygoods1 = Drygoods('Bagpack', 5)
drygoods2 = Drygoods('Paper Towel', 5)
warehouse.add_goods(drygoods1)
warehouse.add_goods(drygoods2)
print(warehouse.describe())
print(warehouse.name)








