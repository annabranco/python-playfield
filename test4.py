from test3 import dictionary, add_ellie, do_everything
# import test4

print(f'names: {list(dictionary.values())}')

add_ellie()
# add_laura() NameError: name 'add_laura' is not defined
names = list(dictionary.items())

for key, value in names:
	print(f'{value} starts with letter {key.upper()}')

print('-' * 30, end=' ')
print('this is imported from test3.py')
do_everything()