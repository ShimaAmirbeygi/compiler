
import parse
import scanner
from parse import *
''' Erfan Asadi : 99170359
    Shima Amirbeigi : 99109347'''
'''https://www.cs.mcgill.ca/~cs520/2021/slides/14-codegen-memfun.pdf'''

if __name__ == '__main__':

    scanner.init_symbol_table()
    Scanner("input.txt").scan_tokens()
    parse.init_first_follow()
    parser= Parser()


