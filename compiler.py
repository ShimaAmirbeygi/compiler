import scanner
from scanner import *
import parser
''' Erfan Asadi : 99170359
    Shima Amirbeigi : 99109347'''
'''Used resources : 
'''


if __name__ == '__main__':
    scanner.init_symbol_table()
    Scanner("input.txt").scan_tokens()
    scanner.save_errors()
    scanner.save_tokens()
    scanner.save_symbol_table()