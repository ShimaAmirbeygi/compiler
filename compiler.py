import scanner
from scanner import *
import parser
from parser import *

''' Erfan Asadi : 99170359
    Shima Amirbeigi : 99109347'''


if __name__ == '__main__':

    scanner.init_symbol_table()
    parser.init_first_follow()
    parser = Parser()


