class Animal(object):
	def __init__(self, name, race):
		self.name = name
		self.race = race
		self.friends = {}

	def give_name(self, new_name):
		self.name = new_name

	def my_name(self):
		if self.name == '':
			thats_me = 'and nobody gave me a name.'
		elif self.name == 'Stranger':
			thats_me = 'and I don\'t wanna tell you my name.'
		else:
			thats_me = f'and my name is {self.name}.'
		return thats_me

	def add_friend(self, friend):
		self.friends[friend.name] = friend.race
		friend.friends[self.name] = self.race
		print(f'\n❤️ {friend.name} and {self.name} are now friends.')

	def remove_friend(self, friend):
		del self.friends[friend.name]
		del friend.friends[self.name]
		print(f'\n💔 {friend.name} and {self.name} are no longer friends. 😞')

	def show_friends(self):
		my_friends = list(self.friends.items())
		print(f'\n{self.name} has {len(my_friends)} friend(s)')
		for name, race in my_friends:
			print(f'- {name}, a {race}')

class Rabbit(Animal):
	def __init__(self, name = ''):
		super(Rabbit, self).__init__(name, 'rabbit')

	def who_are_u(self):
		size = ''
		if self.name == 'Ellie':
			size = 'bigger '
		print(f'<🐰 {self.name}> Hi, I\'m a {size}{self.race}', end = ' ')
		print(super(Rabbit, self).my_name())

class Human(Animal):
	def __init__(self, name = 'Stranger'):
		super(Human, self).__init__(name, 'human')

	def who_are_u(self):
		print(f'<{self.name}> Hi, I\'m a {self.race}', end = ' ')
		print(super(Human, self).my_name())


print('-' * 40)

bunny1 = Rabbit('Bianca')
bunny2 = Rabbit()

human1 = Human('Anna')
human2 = Human()

bunny1.who_are_u()
bunny2.who_are_u()
bunny2.give_name('Ellie')
bunny2.who_are_u()


human1.who_are_u()
human2.who_are_u()
human2.give_name('Laura')
human2.who_are_u()

human1.add_friend(bunny1)
bunny2.add_friend(human1)
bunny1.add_friend(bunny2)
human1.add_friend(human2)

human1.show_friends()
bunny1.show_friends()
bunny2.show_friends()
human2.show_friends()

human1.remove_friend(human2)
human1.show_friends()
human2.show_friends()

print('\n')