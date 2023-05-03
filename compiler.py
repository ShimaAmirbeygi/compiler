import scanner
from scanner import *
import parser
from parser import *

''' Erfan Asadi : 99170359
    Shima Amirbeigi : 99109347'''
'''Used resources : 
'''


if __name__ == '__main__':

    scanner.init_symbol_table()
    # token = ''
    # while token!= '$':
    #     token = my_scanner.get_next_token()
    #     print(token)
    parser.init_first_follow()
    parser = Parser()


