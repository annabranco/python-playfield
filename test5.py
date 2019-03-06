from typing import Dict
import sys


class Animal(object):

    def __init__(self, name, race):
        self.name: str = name
        self.race: str = race
        self.friends: Dict[str, str] = {}

    def give_name(self, new_name: str) -> None:
        self.name: str = new_name

    def my_name(self) -> str:
        if self.name == '':
            thats_me = 'and nobody gave me a name.'
        elif self.name == 'Stranger':
            thats_me = 'and I don\'t wanna tell you my name.'
        else:
            thats_me = f'and my name is {self.name}.'
        return thats_me

    def add_friend(self, friend: object) -> None:

        # their_secondary_friends = []
        # for __my_friend in self.friends:
        #     if self.friends[__my_friend] == 'rabbit':
        #         if __my_friend not in friend.friends:
        #             friend.friends[__my_friend]: str = self.friends.get(
        #                 __my_friend)
        #             their_secondary_friends.append(__my_friend)

        # my_secondary_friends = []
        # for __their_friend in friend.friends:
        #     if friend.friends[__their_friend] == 'rabbit':
        #         if __their_friend not in self.friends:
        #             self.friends[__their_friend]: str = friend.friends.get(
        #                 __their_friend)
        #             my_secondary_friends.append(__their_friend)

        self.friends[friend.name]: str = friend.race
        friend.friends[self.name]: str = self.race

        self.inform(f'❤️  {self.name} and {friend.name} are now friends.')
        # if len(their_secondary_friends) > 0:
        #     print(f'\t- {friend.name} also became friend of:')
        #     for __friend in their_secondary_friends:
        #         print(f'\t\t🐰 {__friend}')
        #     sys.stdout.write('\n')
        # if len(my_secondary_friends) > 0:
        #     print(f'\t- {self.name} also became friend of:')
        #     for __friend in my_secondary_friends:
        #         print(f'\t\t🐰 {__friend}')
        #     sys.stdout.write('\n')

    def remove_friend(self, friend) -> None:
        del self.friends[friend.name]
        del friend.friends[self.name]
        return self.inform(f'💔  {friend.name} and {self.name} are no longer friends. 😞')

    def show_friends(self) -> None:
        my_friends = list(self.friends.items())
        print(f'\t{self.name} has {len(my_friends)} friend(s):')
        for name, race in my_friends:
            print(f'\t\t- {name}, a {race}')
        sys.stdout.write('\n')

    def say(self, what) -> None:
        print(f'\t<{self.name.upper()}> {what}\n')

    def inform(self, what) -> None:
        print(f'\t{what}\n')


class Rabbit(Animal):

    def __init__(self, name=''):
        super(Rabbit, self).__init__(name, 'rabbit')

    def who(self):
        size = ''
        if self.name == 'Ellie':
            size = 'bigger '
        return self.say(f'Hi, I\'m a {size}{self.race} {super(Rabbit, self).my_name()}')

    def say(self, what) -> None:
        print(f'\t<🐰 {self.name.upper()}> {what}\n')


class Human(Animal):

    def __init__(self, name='Stranger'):
        super(Human, self).__init__(name, 'human')

    def who(self):
        return self.say(f'Hi, I\'m a {self.race} {super(Human, self).my_name()}')

# x = property(z,y)


print('-' * 40)


def _print(what: str):
    print(f'>> {what}')


_print("anna = Human('Anna')")
anna = Human('Anna')
_print("bunny1 = Rabbit('Bianca')")
bunny1 = Rabbit('Bianca')
_print("bunny2 = Rabbit()")
bunny2 = Rabbit()
_print("laura = Human()")
laura = Human()

_print("anna.who()")
anna.who()
_print("bunny1.who()")
bunny1.who()
_print("bunny2.who()")
bunny2.who()
_print("bunny2.give_name('Ellie')")
bunny2.give_name('Ellie')
_print("bunny2.who()")
bunny2.who()
_print("laura.who()")
laura.who()
_print("laura.give_name('Laura')")
laura.give_name('Laura')
_print("laura.who()")
laura.who()

_print("anna.add_friend(bunny1)")
anna.add_friend(bunny1)
_print("anna.add_friend(bunny2)")
anna.add_friend(bunny2)
_print("bunny1.add_friend(bunny2)")
bunny1.add_friend(bunny2)
_print("anna.add_friend(laura)")
anna.add_friend(laura)

_print("anna.show_friends()")
anna.show_friends()
_print("bunny1.show_friends()")
bunny1.show_friends()
_print("bunny2.show_friends()")
bunny2.show_friends()
_print("laura.show_friends()")
laura.show_friends()

_print("laura.remove_friend(anna)")
anna.remove_friend(laura)
_print("anna.show_friends()")
anna.show_friends()
_print("laura.show_friends()")
laura.show_friends()
