from .provider.bitwarden_store import BitwardenStore
from .provider.keepass_store import KeepassStore
from colorama import init, Back, Style
from .get_char import GetChar
from os import system, name
import logging
import pyperclip
import argparse


def does_match(se, search=''):
    if search.lower() in se.name.lower():
        return True

    for add in se.addresses:
        if search.lower() in add.lower():
            return True

    return False


def filter_entries(store, search=''):
    return list(filter(lambda e: does_match(e, search), store.get_and_cache_simple_entries()))


def paint(search='', entries=[], idx=0):
    screen_clear()
    print('Search: ' + search)
    for x, entry in enumerate(entries):
        if x == idx:
            print(Back.MAGENTA + str(entry) + Style.RESET_ALL)

        else:
            print(str(entry))


def screen_clear():
    if name == 'nt':
        system('cls')  # windows
    else:
        system('clear')  # unix


def start_input_loop(store):
    char_list = []
    select_idx = 0
    get_char = GetChar()
    while True:
        search = ''.join(char_list)
        entries = filter_entries(store, search)
        paint(search=search, entries=entries, idx=select_idx)
        ch = get_char()
        logging.debug('char repr: ' + repr(ch))
        if ch == '\x03':  # control-c
            break
        elif ch == '\x7f':  # backspace
            select_idx = 0
            if len(char_list) > 0:
                char_list.pop(-1)
        elif ch == '\r' or ch == '\n':
            if len(entries) > select_idx:
                return entries[select_idx]
        elif ch == '\x1b':
            direction = get_char() + get_char()
            if direction == '[B' and select_idx < len(entries) - 1:
                select_idx += 1
            elif direction == '[A' and select_idx > 0:
                select_idx -= 1
        else:
            char_list += ch
            select_idx = 0
        logging.debug('char_list' + str(char_list))


def main():
    init()

    parser = argparse.ArgumentParser(description='Password Lookup')

    parser.add_argument('-f', action='store', dest='file',
                        help='KeePassFile')

    parser.add_argument('-c', action='store_true', default=False,
                        dest='clear_session',
                        help='Clear session')
    result = parser.parse_args()
    if not result.file:
        store = BitwardenStore(clear_session=result.clear_session)
    else:
        store = KeepassStore(result.file, clear_session=result.clear_session)

    filter_entries(store)
    entry = start_input_loop(store)
    if entry is not None:
        print('copied password!')
        pyperclip.copy(entry.password)


if __name__ == '__main__':
    main()
