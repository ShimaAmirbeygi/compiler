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
        self.runtime_stack = list()
        self.current_scope = 0
        self.return_stack = list()
        self.index = 0
        self.temp_address = 500
        self.break_stack = list()
        self.operations_dict = {'+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}

    # this function call action of each symbol
    def call_routine(self, symbol, lookahead):
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
        self.SS.append(self.index)  # to jump over for non-main functions
        self.index += 1
        self.SS.append(function_name)
        # mark the table before adding args
        symbol_table['ids'].append('params->')

    # when params finish add function to symbol table if a function with same name
    # but have different params recognize in this method
    def record_params(self, lookahead):
        return_address = self.get_temp()
        current_index = self.index  # to jump over for non-main functions
        return_value = self.get_temp()
        self.SS.append(return_value)
        self.SS.append(return_address)
        func_id = self.SS[-3]  # function name
        args_start_idx = symbol_table['ids'].index('params->')
        # print(symbol_table['ids'], args_start_idx)
        func_args = symbol_table['ids'][args_start_idx + 1:]  # 8 for params->
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
        temp = self.get_temp()
        self.insert_code('MULT', '#4', id, temp)
        self.insert_code('ADD', f'#{array_address}', temp, temp)
        self.SS.append(f'@{temp}')

    def assign(self, lookahead):
        self.insert_code('ASSIGN', self.SS[-1], f'{self.SS[-2]}')
        self.SS.pop()

    def pop(self, lookahead):
        self.SS.pop()

    def implicit_output(self, lookahead):
        if self.SS[-2] == 'output':
            self.insert_code('PRINT', f'{self.SS.pop()}')

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
        if self.SS[-3] != 'main':
            return_address = self.SS[-1]
            self.insert_code('JP', f'@{return_address}')
        # if self.SS[-1] == 'main':
        #     self.save_program_block()

    # def save_program_block(self):
    #     i = 0
    #     with open('output.txt', 'w') as f:
    #         for record in self.PB:
    #             f.write(f'{i}\t' + f'{self.PB[i]}\n')
    #             i += 1
    #     with open('semantic_errors.txt', 'w') as f:
    #         f.write('The input program is semantically correct.\n')

    def label(self, lookahead):
        self.SS.append(self.index)

    """saves index to be later filled with a jump to after the scope"""

    def break_loop(self, lookahead):
        self.break_stack.append(">>>")
        self.break_stack.append(self.index)
        self.index += 1

    """fills PB[saved index] with a jump to current index and ends the scope"""

    def handle_breaks(self, lookahead):
        if (len(self.break_stack) > 0):
            latest_block = len(self.break_stack) - self.break_stack[::-1].index('>>>') - 1
            for item in self.break_stack[latest_block + 1:]:
                self.PB[item] = f'(JP, {self.index}, , )'
            self.break_stack = self.break_stack[:latest_block]

    def mult(self, lookahead):
        res = self.get_temp()
        self.insert_code('MULT', self.SS[-1], self.SS[-2], res)
        self.SS.pop()
        self.SS.pop()
        self.SS.append(res)

    def until(self, lookahead):
        condition = self.SS.pop()
        destination = self.SS.pop()
        self.insert_code('JPF', condition, destination)

    def save(self, lookahead):
        self.SS.append(self.index)
        self.index += 1

    def jpf_save(self, lookahead):
        dest = self.SS.pop()
        src = self.SS.pop()
        self.PB[dest] = f'(JPF, {src}, {self.index + 1}, )'
        self.SS.append(self.index)
        self.index += 1

    def jump(self, lookahead):
        dest = int(self.SS.pop())
        self.PB[dest] = f'(JP, {self.index}, , )'

    def push_index(self, lookahead):
        self.SS.append(f'#{self.index}')

    # Function call and return
    def finish_function(self, lookahead):
        """in create_record we saved an instruction for now,
        so that non-main functions are jumped over.
        Also, we need to clean up the mess we've made in SS.
        """
        self.SS.pop(), self.SS.pop(), self.SS.pop()
        # all this shit only to exclude main from being jumped over
        for item in symbol_table['ids'][::-1]:
            if item[1] == 'function':
                if item[0] == 'main':
                    self.PB[self.SS.pop()] = f'(ASSIGN, #0, {self.get_temp()}, )'
                    return
                break
        self.PB[self.SS.pop()] = f'(JP, {self.index}, , )'

    def call_function(self, lookahead):
        """Does the following:
                    1. assigns inputs to args.
                    2. sets where the func must return to.
                    3. jumps to the beginning of the function.
                    4. saves the result (if any) to a temp and pops
                       everything about the function and pushes the temp.
                """
        if self.SS[-1] != 'output':
            args, attributes = [], []

            for item in self.SS[::-1]:

                if isinstance(item, list):
                    attributes = item
                    break
                args = [item] + args
            # assign each arg
            for var, arg in zip(attributes[1], args):
                self.insert_code('ASSIGN', arg, var[2])
                self.SS.pop()  # pop each arg
            for i in range(len(args) - len(attributes[1])):
                self.SS.pop()
            self.SS.pop()  # pop func attributes
            # set return address
            self.insert_code('ASSIGN', f'#{self.index + 2}', attributes[2])
            # jump
            self.insert_code('JP', attributes[-1])
            # save result to temp
            result = self.get_temp()
            self.insert_code('ASSIGN', attributes[0], result)
            self.SS.append(result)

    def save_return(self, lookahead):
        """called by each return. Saves two instructions:
                one for assigning the return value,
                and one for jumping to the caller
                """
        self.return_stack.append((self.index, self.SS[-1]))
        self.SS.pop()
        self.index += 2

    def define_array_argument(self, lookahead):
        temp = symbol_table['ids'][-1]
        del symbol_table['ids'][-1]
        symbol_table['ids'].append((temp[0], 'int*', temp[2], temp[3]))

    def create_return(self, lookahead):
        """indicates new function so that every report between this and #end_return
                sets the return value and jumps to the address set by the caller
                """
        self.return_stack.append('>>>')

    def end_return(self, lookahead):
        """called at the end of the function, fills the gaps created by returns"""
        latest_func = len(self.return_stack) - self.return_stack[::-1].index('>>>') - 1
        return_value = self.SS[-2]
        return_address = self.SS[-1]
        for item in self.return_stack[latest_func + 1:]:
            self.PB[item[0]] = f'(ASSIGN, {item[1]}, {return_value}, )'
            self.PB[item[0] + 1] = f'(JP, @{return_address}, , )'
        self.return_stack = self.return_stack[:latest_func]
