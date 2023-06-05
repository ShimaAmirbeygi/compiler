from scanner import *
semantic_errors = list()

class CodeGenerator:
    '''a program that run the code generator for the compiler'''

    def push_scope(self,lookahead):
       self.current_scope+=1

    def __init__(self):
        # semantic stack
        self.SS = list()
        # code segment
        self.PB = dict()



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

    #   pop the last element of stack and
    def define_variable(self, lookahead):
        var_id = self.SS.pop()
        self.is_void(var_id)

        address = self.get_temp()
        symbol_table['ids'].append((var_id, 'int', address, self.current_scope))


    def push_num(self, lookahead):
        self.SS.append(f'#{lookahead[2]}')


    def define_array (self,lookahead):
        var_id = self.SS.pop()
        self.is_void(var_id)
        address = self.get_temp()
        symbol_table['ids'].append((var_id, 'array', address, self.current_scope))

    # define function parameters
    def define_params(self, lookahead):

        function_name = self.SS.pop()
        self.SS.append(self.index)  # to jump over for non-main functions
        self.index += 1
        self.SS.append(function_name)
        # mark the table before adding args
        symbol_table['ids'].append('params->')

    # when params finish add function and params to symbol table
    def record_params(self,lookahead):
        return_address = self.get_temp()
        current_index = self.index  # to jump over for non-main functions
        return_value = self.get_temp()
        self.SS.append(return_value)
        self.SS.append(return_address)
        func_id = self.SS[-3]#function name
        args_start_idx = symbol_table['ids'].index('params->')
        func_args = symbol_table['ids'][args_start_idx + 8:] # 8 for params->
        symbol_table['ids'].pop(args_start_idx)
        symbol_table['ids'].append((func_id, 'func', [return_value, func_args, return_address, current_index], self.current_scope))