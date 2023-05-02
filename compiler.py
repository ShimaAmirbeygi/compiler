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
    my_scanner = Scanner("input.txt")
    my_scanner.init_input()
    print(type(my_scanner))
    parser.init_first_follow()
    parser = Parser(scanner)


