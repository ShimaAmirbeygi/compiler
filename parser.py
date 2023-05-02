import scanner
from scanner import *
from anytree import AnyNode, RenderTree


root = AnyNode(id="Program")
# s0 = AnyNode(id="sub0", parent=root)
syntax_errors = dict()
parse_tree = list()
first = dict()
follow = dict()
predict = dict()
rules = 77 * [0]


def save_syntax_errors():
    with open('syntax_errors.txt', 'w') as f:
        if syntax_errors:
            f.write('\n'.join(['#' + f'{line_no + 1}' + ' : syntax error, ' + f'{error}'
                           for line_no, error in syntax_errors.items()]))
        else:
            f.write('There is no syntax error.')

def save_parse_tree():
    with open('parse_tree.txt', 'w') as f:
        f.write(RenderTree(root).by_attr('id'))


def init_first_follow():
    with open('first_set.txt', 'r') as f:
        for line in f.read().splitlines():
            elements = line.split('\t', 1)
            first[elements[0]] = elements[1].split(', ')
    with open('follow_set.txt', 'r') as f:
        for line in f.read().splitlines():
            elements = line.split('\t', 1)
            follow[elements[0]] = elements[1].split(', ')

    with open("rules_number.txt") as f1, open("predict_set.txt") as f2:
        for x, y in zip(f1, f2):
            elements = x.strip().split('\t', 1)
            rules[int(elements[0])] = elements[1]
            rule = elements[1].split(' → ', 1)
            left = rule[0]
            right = rule[1]
            if left not in predict:
                predict[left] = {}
            y = y.strip().split(', ')
            for first_for_rule in y:
                predict[left][first_for_rule] = right.split(' ')

    print(predict)


def is_terminal(a):
    return True

class Parser:
    def __init__(self):
        self.my_scanner = Scanner("input.txt")
        self.my_scanner.init_input()
        self.line_number = 0 # shomare khat az token begir
        self.LA = str()

    def updat_LA(self):
        token = self.my_scanner.get_next_token()


    def DFA(self, nt_node, depth):
        # nt_node type string hast anytree ash ghabl az seda zadan sakhte shode

        # unexpected EOF ham darim
        # path ro az roo predict set peyda mikonam , ye for mizanam ro azash

        # next = self.predict[nt_node][self.LA]
        # path = next +

        # aval masiro peyda kon 1- sync 2- path vogood dare 3- khali


        path = 3
        for next in path:

            if next:
                if not is_terminal(next):
                    next = AnyNode(id="nt_node", parent=root)
                    self.DFA(self, next, depth + 1)
                elif self.LA == next:
                    self.LA = self.scanner.scan_next_token()
                    '''next ro az ro path peyda kon '''
                else:
                    syntax_errors[self.line_number] = 'missing '.join(self.LA)
                    '''next ro az ro path peyda kon '''

            elif next == 'sync':
                syntax_errors[self.line_number] = 'missing '.join(nt_node)
                return
            else:
                # empty
                syntax_errors[self.line_number] = 'illegal '.join(self.LA)
                self.LA = self.scanner.scan_next_token()

