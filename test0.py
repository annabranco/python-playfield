from sys import argv

userList = list(open('names.txt').read().split(','))

print(userList)

if len(argv) <= 1:
    print('You didn\'t identify yourself.')
    user = input('Who are you, stranger? ')
else:
    filename, user = argv

visits = 0
for name in userList:
	if name == user:
		visits += 1

if visits == 0:
	print(f'Hola {user}!')
	# print('Hola %s!' % user)
	# print('Hola %s' % user + '!')
elif visits == 1:
	print(f'Welcome back, {user}!')
else:
	print(f'Welcome back, {user}!')
	print(f'You\'ve logged another {visits} times. You really like me, don\'t ya? ;)')

newUserList = open('names.txt', 'a')
newUserList.write(f',{user}')
# newUserList.write(str(userList))
excuse = ''
if visits > 0:
	excuse = f'Sorry {user}, I was not programmed yet to recall it... '

another_user = input('{} who is yout best friend? '.format(excuse))

i = 1
while another_user == user and i == 1:
    print(f'Sorry {user}, but you gave your own name.')
    another_user = input('Who is your bestie? ')
    i += 1

if another_user == user:
    print('So you have a best friend with your own name?? Great! ^^')
    print('or maybe you are your own best friend... it\'s cool, I guess...')
elif another_user == 'you':
		print(f'Oh {user}... am I your bestie?? I\'d cry if I could... :~D')
else:
    print('So, {} is your bestie! I\'m glad to read that!'.format(another_user))
