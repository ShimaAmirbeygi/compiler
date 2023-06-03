class CodeGenerator:
    '''a program that run the code generator for the compiler'''

    def push_scope(self,lookahead):
       self.current_scope+=1;

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
