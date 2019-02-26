class Rabbit:
    name = 'Bianca'

    def change_name(self, new_name):
        self.name = new_name


rabbit1 = Rabbit()
print(rabbit1.name)

rabbit2 = Rabbit()
rabbit2.change_name('Ellie')
print(rabbit2.name)

rabbit3 = rabbit2
rabbit3.change_name('Anna')
print(rabbit3.name, rabbit2.name)


class RabbitWithName:

    def __init__(self, name):
        self.name = name

    def change_name(self, new_name):
        self.name = new_name


rabbit1 = RabbitWithName('Bianca')
print(rabbit1.name)

rabbit2 = RabbitWithName('Anna')
rabbit2.change_name('Ellie')
print_her_name = 'print(rabbit2.name)'

exec(print_her_name)
