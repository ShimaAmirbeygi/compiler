
import pars
import scanner
from pars import *
''' Erfan Asadi : 99170359
    Shima Amirbeigi : 99109347'''


if __name__ == '__main__':

    scanner.init_symbol_table()
    Scanner("input.txt").scan_tokens()
    scanner.save_symbol_table()
    scanner.save_tokens()
    pars.init_first_follow()
    parser= Parser()


