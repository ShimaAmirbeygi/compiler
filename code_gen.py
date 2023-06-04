from scanner import *
semantic_errors = list()

class CodeGenerator:
    '''a program that run the code generator for the compiler'''

    def push_scope(self,lookahead):
       self.current_scope+=1

    def __init__(self):
        # scope segment
        self.SS = list()
        # code segment
        self.PB = dict()
        # data segment
        self.DS = dict()
        # stack segment


        self.break_stack = list()
        self.current_scope = 0
        self.return_stack = list()
        self.index = 0
        self.temp_address = 100
        self.operations_dict = {'+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}



    # this function call action of each symbol
    def call_function(self, symbol, lookahead):
           self.__getattribute__(symbol)(lookahead)

    def insert_code(self, part1, part2, part3='', part4=''):
        self.PB[self.index] = f'({part1}, {part2}, {part3}, {part4})'
        self.index += 1

    def get_temp(self, count=1):
        address = str(self.temp_address)
        for _ in range(count):
            self.insert_code('ASSIGN', '#0', str(self.temp_address))
            self.temp_address += 4
        return address

    def get_address(self, var_id):
        if var_id in self.DS.keys():
            return self.DS[var_id]
        else:
            return None
    def is_void(self,var_id):
        if var_id =="void":
            semantic_errors.append(f'#{self.id_type[0]} : Semantic Error! Illegal type of void for \'{var_id}\'.')


    def pid(self, lookahead):
        self.SS.append(lookahead)


    def get_id_type(self, lookahead):
        self.id_type = lookahead