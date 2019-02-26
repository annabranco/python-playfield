from random import randint
from sys import argv

argv = argv[1:]
print(argv)
if len(argv) == 0:
	action = input('> ')
else:
	action = argv[0]

Hero = {
	'attack': 5,
	'defense': 5,
	'hp': 5
}

monster1 = {
	'name': 'Ugly Monster',
	'attack': 5,
	'defense': 5,
	'hp': 2,
	'status': ['angry', 3]
}

enemy = monster1

# COMBAT - ATTACK
def attack(bonus, enemy):
	difficult = enemy['defense']
	base_attack = Hero['attack'] + bonus
	i = 0
	rolls = []
	while i < base_attack:
		rolls.append(randint(1, 10))
		i += 1
	successes = 0
	print(rolls)
	for roll in rolls:
		if roll >= difficult:
			successes += 1
	print(f'successes: {successes}', end=' ')
	successes = successes - manage_critical_fails(rolls) + manage_critical_successes(rolls)
	print(f'- total: {successes}')
	if successes < 0:
		epic_fail(successes)
	elif successes > 1:
		cause_damage(successes, enemy)
	else:
		missed(enemy)

def manage_critical_fails(rolls):
	critical_fails = 0
	for roll in rolls:
		if roll == 1:
			critical_fails += 1
	print('critical_fails', critical_fails, end=' ')
	return critical_fails

def manage_critical_successes(rolls):
	critical_successes = 0
	for roll in rolls:
		if roll == 10:
			critical_successes += 1
	print('critical_successes',critical_successes)
	return critical_successes

def	epic_fail(successes):
	print('You lose your balance and fall on the ground.')

def cause_damage(successes, enemy):
	hp = enemy['hp']
	print(hp)
	new_hp = hp - successes
	if new_hp <= 0:
		enemy['hp'] = ['dead', 0]
		print(f'You give a mortal thrust of your blade and {enemy['name']} falls dead.')
		print('You win!')
		exit(0)
	elif new_hp <= hp / 3:
		enemy['hp'] = new_hp
		enemy['hp'] = ['severily wounded', 1]
		print(f'You slash your sword causing a great damage on {enemy['name']}. It is badly hurt'.)
	else:
		enemy['hp'] = new_hp
		enemy['hp'] = ['wounded', 2]
		print(f'You strike a blow on {enemy['name']}, causing some blood to spill'.)
	next_round()

def	missed(enemy):
	print(f'{enemy['name']} blocks your attack.')


# COMBAT - BEGINNING
def initiative(bonus, enemy):
	pass

# COMBAT - DEFENDING
def defend(bonus, enemy):
	pass

# ACTIONS - CINEMATICS
print(f'You see {enemy['name']}.)
next_round(enemy)

def next_round(enemy):
	print(f'{enemy['name']} is {enemy.status[0]}. What do you do?')

#  action = input('> ')

if action == 'attack':
	print(f'You draw your sword and strike before {enemy['name']} has a chance to understand what is happening.')
	attack(2, enemy)
elif action == 'wait':
	print(f'You wait to see the reaction of the {enemy['name']}. He draws a club and comes to attack you.')
	initiative(0, enemy)
elif action == 'defend':
	print(f'You put yourseld on a defensive stance while the {enemy['name']} draws a club and comes to attack you.')
	defend(2, enemy)
