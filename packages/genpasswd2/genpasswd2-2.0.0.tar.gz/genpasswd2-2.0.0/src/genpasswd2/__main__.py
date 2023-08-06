"""genpasswd - Generate Random Passwords

Usage:
  genpasswd [LENGTH] [-hvdlup]

Arguments:
  LENGTH  Password length

Options:
  -h --help     Show this screen
  -v --verbose  Show password and it's length
  -d            Exclude digits from the password
  -l            Exclude lowercase letters from the password
  -u            Exclude uppercase letters from the password
  -p            Exclude punctuation characters from the password

"""
from docopt import docopt
from random import choice
from string import digits, ascii_lowercase, ascii_uppercase, punctuation
import pyperclip
import sys


def main(arguments):
    chars = [digits, ascii_lowercase, ascii_uppercase, punctuation]
    length = 16

    if arguments['LENGTH']:
        try:
            length = int(arguments['LENGTH'])
        except ValueError:
            print(f'LENGTH should be integer')
            sys.exit(2)

        if length <= 0:
            print('LENGTH should be more than 0')
            sys.exit(2)

    if arguments['-d']:
        chars.remove(digits)

    if arguments['-l']:
        chars.remove(ascii_lowercase)

    if arguments['-u']:
        chars.remove(ascii_uppercase)

    if arguments['-p']:
        chars.remove(punctuation)
        
    if not chars:
        print('You excluded everything.')
        sys.exit(2)

    password = ''.join(choice(choice(chars)) for _ in range(length))
    pyperclip.copy(password)

    if arguments['--verbose']:
        print(f'Generated password: \33[1;30;42m{password}\33[0;0m')
        print(f'Password length: \33[1;32m{length}\33[0;0m')

    print('Password copied to clipboard.')


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
