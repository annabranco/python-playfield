from sys import argv

argv = argv[1:]

if argv:
    [user] = argv
else:
    user = 'Anna'

print(user)


def myfunc1():
    # global x
    x = "Anna"

    def myfunc2():
        nonlocal x
        x = "hello"
    return x


print(myfunc1())


try:
    x
except NameError:
    print("You have a variable that is not defined.")
except TypeError:
    print("You are comparing values of different type")
except:
    print("Something else went wrong")
else:
    print('variable x exists')


if 'x' not in globals():
    raise Exception("Sorry, X is not declared on global scope")
