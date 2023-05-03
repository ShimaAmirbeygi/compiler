import scanner
from scanner import *
from anytree import AnyNode, RenderTree


root = AnyNode(id="Program")
# s0 = AnyNode(id="sub0", parent=root)
syntax_errors = defaultdict(list)
parse_tree = list()
first = dict()
follow = dict()
predict = dict()
rules = 77 * [0]


def save_syntax_errors():
    with open('syntax_errors.txt', 'w') as f:
        if syntax_errors:
            f.write('\n'.join(['#' + f'{line_no}' + ' : syntax error, ' + f'{error}'
                           for line_no, errors in syntax_errors.items()
                               for error in errors]))
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

    # print(predict)

def finish():
    save_parse_tree()
    save_syntax_errors()
    exit()


def is_terminal(a):
    if a in follow.keys():
        return False
    return True

def print_token(t):
    if type(t) == str:
        return t
    return '(' + t[0] + ', ' + t[1] + ')'

class Parser:
    def __init__(self):
        self.token = None
        self.my_scanner = Scanner("input.txt")
        self.my_scanner.init_input()
        self.line_number = 0 # shomare khat az token begir
        self.LA = str()
        # print(rules)
        # print(predict)
        self.updat_LA()
        self.DFA(root)
        finish()

    def updat_LA(self):
        if self.LA == '$':
            syntax_errors[self.line_number].append('Unexpected EOF')
            finish()
        self.token = self.my_scanner.get_next_token()
        # print('tokennn', self.token)
        if type(self.token) == str:
            '''LA = $'''
            self.LA = self.token
        else:
            self.line_number = self.token[0]
            self.token = self.token[1]
            self.LA = scanner.get_type(self.token[1])



    def DFA(self, nt_node):
        # nt_node type anytree hast
        # aval masiro peyda kon 1- sync 2- empty 3- epsilon 4-path vogood dare

        state = nt_node.id
        if self.LA in predict[state]:
            path = predict[state][self.LA]

            if len(path) == 1 and path[0] == 'ε':
                '''epsilon'''
                AnyNode(id="epsilon", parent=nt_node)
                return
            else:
                for next in path:
                    if not is_terminal(next):
                        next_nt_node = AnyNode(id=next, parent=nt_node)
                        self.DFA(next_nt_node)
                    elif self.LA == next:
                        AnyNode(id=print_token(self.token), parent=nt_node)
                        # if self.LA == '$' in bayad khodesh rokh bede?
                        self.updat_LA()
                    else:
                        '''anytree bayad (type(next),next) ro chaap kone ?'''
                        syntax_errors[self.line_number].append('missing ' + next)
        else:
            '''delete nt_node'''

            if self.LA in follow[state]:
                '''sync'''
                nt_node.parent = None
                syntax_errors[self.line_number].append('missing ' + state)
                return
            else:
                '''empty '''
                # scanner.get_token_type()
                syntax_errors[self.line_number].append('illegal ' + self.LA)
                self.updat_LA()
                self.DFA(nt_node)
                return
