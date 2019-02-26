dictionary = {'a': 'Anna', 'd': 'Debra', 'j': 'Jeannie'}

def add_laura():
	dictionary[0] = 'Laura'

def add_ellie():
	dictionary['e'] = 'Ellie'

def rem_laura():
	del dictionary[0]

def print_new_list():
	name_list = list(dictionary.items())

	for key, value in name_list:
		print(f'letter {key} has name {value}')

	f = dictionary.get('f') # returns None
	print(f)
	if not f:
		print('sorry, no "F"')

	s = dictionary.get('s', 'Sarah') # Default value
	print(s)

def do_everything():
	add_laura()
	add_ellie()
	print(dictionary)
	rem_laura()
	print(dictionary)
	print_new_list()

# do_everything()