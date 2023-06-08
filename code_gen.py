from operator import itemgetter

from scanner import *

semantic_errors = list()


class CodeGenerator:
    """a program that run the code generator for the compiler"""

    def push_scope(self):
        self.current_scope += 1

    def __init__(self):
        # semantic stack
        self.SS = list()
        # code segment
        self.PB = dict()

        self.break_stack = list()
        self.current_scope = 0
        self.return_stack = list()
        self.index = 0
        self.temp_address = 500
        self.operations_dict = {'+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}

    # this function call action of each symbol
    def call_function(self, symbol, lookahead):
        self.__getattribute__(symbol)(lookahead)

    def insert_code(self, part1, part2, part3='', part4=''):
        self.PB[self.index] = f'({part1}, {part2}, {part3}, {part4})'
        self.index += 1

    def get_temp(self, count=1):
        address = str(self.temp_address)
        self.insert_code('ASSIGN', '#0', str(self.temp_address))
        self.temp_address += count * 4
        return address

    def get_address(self, var_id):
        if var_id in self.DS.keys():
            return self.DS[var_id]
        else:
            return None

    def is_void(self, var_id):
        if var_id == "void":
            semantic_errors.append(f'#{self.id_type[0]} : Semantic Error! Illegal type of void for \'{var_id}\'.')

    def pid(self, lookahead):
        self.SS.append(lookahead[1][1])

    def get_id_type(self, lookahead):
        self.id_type = lookahead[1][1]

    #   pop the last element of stack and
    def define_variable(self, lookahead):
        var_id = self.SS.pop()
        self.is_void(var_id)
        address = self.get_temp()
        symbol_table['ids'].append((var_id, 'int', address, self.current_scope))

    def push_num(self, lookahead):
        self.SS.append(f'#{lookahead[1][1]}')

    def define_array(self, lookahead):
        var_id = self.SS.pop()
        function_name = self.SS.pop()
        self.is_void(var_id)
        address = self.get_temp(int(var_id[1:]))
        symbol_table['ids'].append((function_name, 'array', address, self.current_scope))

    # its come before  params and ( and append a params-> to symbol table and after record_params record all params after patams-> in symbol table
    def define_params(self, lookahead):

        function_name = self.SS.pop()
        self.SS.append(function_name)
        # mark the table before adding args
        symbol_table['ids'].append('params->')

    # when params finish add function to symbol table if a function with same name
    # but have different params recognize in this method
    def record_params(self, lookahead):
        return_address = self.get_temp()
        current_index = self.index  # to jump over for non-main functions
        return_value = self.get_temp()
        # self.SS.append(return_value)
        # self.SS.append(return_address)
        func_id = self.SS[-1]  # function name
        args_start_idx = symbol_table['ids'].index('params->')
        func_args = symbol_table['ids'][args_start_idx + 8:]  # 8 for params->
        symbol_table['ids'].pop(args_start_idx)
        symbol_table['ids'].append(
            (func_id, 'func', [return_value, func_args, return_address, current_index], self.current_scope))

    def main(self, lookahead):
        self.insert_code('ASSIGN', '#4', '0')
        self.insert_code('JP', '2')

    def increase_scope(self, lookahead):
        self.current_scope += 1

    def decrease_pop_scope(self, lookahead):
        for record in symbol_table['ids'][::-1]:
            if record[3] == self.current_scope:
                del symbol_table['ids'][-1]
        self.current_scope -= 1

    def search_in_symbol_table(self, id, scope_num=0):

        for record in symbol_table['ids'][::-1]:
            if id == record[0] and record[3] <= scope_num:
                return record[0]
        return False

    def pid_address(self, lookahead):
        flag = 0
        if self.search_in_symbol_table(lookahead[1][1], self.current_scope) or lookahead[1][1] == 'output':
            flag = 1
        if flag == 0:
            print(lookahead)
            semantic_errors.append(f'#{lookahead[0]} : Semantic Error! \'{lookahead[1][1]}\' is not defined.')
        id = self.search_in_symbol_table(lookahead[1][1], self.current_scope)
        if lookahead[1][1] == 'output':
            self.SS.append('output')
        for record in symbol_table['ids'][::-1]:
            if id == record[0]:
                self.SS.append(record[2])

    def array_index(self, lookahead):
        id = self.SS.pop()
        array_address = self.SS.pop()
        temp, result = self.get_temp(), self.get_temp()
        self.insert_code('MULT', '#4', id, temp)
        self.insert_code('ASSIGN', f'{array_address}', f'@{result}')
        self.insert_code('ADD', result, temp, result)
        self.SS.append(result)

    def assign(self, lookahead):
        self.insert_code('ASSIGN', self.SS[-1], f'{self.SS[-2]}')
        self.SS.pop()

    def pop(self, lookahead):
        self.SS.pop()

    def implicit_output(self, lookahead):
        if self.SS[-2] == 'output':
            self.insert_code('PRINT', f'@{self.SS.pop()}')

    def push_operator(self, lookahead):
        self.SS.append(lookahead[1][1])

    def save_operation(self, lookahead):
        operand_2 = self.SS.pop()
        operator = self.SS.pop()
        operand_1 = self.SS.pop()
        address = self.get_temp()
        self.insert_code(self.operations_dict[operator], operand_1, operand_2, address)
        self.SS.append(address)

    def return_anyway(self, lookahead):
        """places a jump at the end of function. just in case it hasn't already"""
        if self.SS[-1] == 'main':
            self.save_program_block()

    def save_program_block(self):
        i =0
        with open('output.txt', 'w') as f:
            for record in self.PB:
               f.write(f'{i}    '+f'{self.PB[i]}\n')
               i+=1