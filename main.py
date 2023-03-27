import time
from copy import deepcopy

DEBUG = False

class Node:
    def __init__(self, _name):
        self.name = _name
        self.transitions = []
        self.is_final = True if _name in final_states else False

    def add_transition(self, t):
        self.transitions += [t]

    def __str__(self):
        ret = f'Node {self.name}\nTransitions:\n'
        for t in self.transitions:
            ret += str(t) + '\n'
        return ret


class Transition:
    def __init__(self, _from, _to, symbol, stack, add):
        self._from = _from
        self._to = _to
        self.symbol = symbol
        self.stack = stack
        self.add = add

    def __str__(self):
        return f"{self._from.name} -> {self._to.name} | {self.symbol}, {self.stack} | {self.add}"


class NPDA:
    def __init__(self, nodes, starting_node, l_symbol, initial_stack):
        self.nodes = deepcopy(nodes)
        self.lam = l_symbol
        self.starting_node = starting_node
        self.current_node = starting_node
        self.word = None
        self.initial_stack = initial_stack
        self.stack = [initial_stack]
        self.found = []

    def check(self, word):
        print(f"input {word}")
        self.found = []
        self.word = deepcopy(word)
        self.current_node = self.starting_node
        self.stack = [self.initial_stack]

        self.advance([self.initial_stack], deepcopy(word))
        print()

    def advance(self, stack, word, level=0):
        if self.current_node.is_final:
            word_parsed = self.word[:len(self.word) - len(word)]
            if word_parsed not in self.found:
                self.found += [word_parsed]
                print(f"{word_parsed} acceptat de npda")
                # print(word)

        # if len(word) == 0 or len(self.stack) == 0:
        #     return

        # verificam toate tranzitiile
        for t in self.current_node.transitions:
            # verificam daca simbolul este la fel cu primul ramas in cuvant (sau simbolul pe tranzitie sa fie lambda) si stiva sa fie buna
            # daca da, facem tranzitia
            if (t.symbol == self.lam or (len(word) and t.symbol == word[0])) and t.stack == stack[-1]:
                # taiem din cuvant
                new_word = deepcopy(word)
                if t.symbol != self.lam:
                    new_word = new_word[1:]
                # scoatem de pe stack
                new_stack = deepcopy(stack)
                new_stack.pop()
                for s in reversed(t.add):
                    if s != self.lam:
                        new_stack += [s]
                # schimbam nodul curent
                self.current_node = t._to

                if DEBUG:
                    pprint(t, level)
                    pprint(stack, level)
                    pprint(new_stack, level)
                    pprint(self.word[:len(self.word) - len(word)], level)
                    pprint(self.word[:len(self.word) - len(new_word)], level)
                    # print(new_word)
                    pprint("----------------")
                self.advance(new_stack, new_word, level+1)

def pprint(txt, lvl=0):
    print(f'{" " * lvl * 4}{txt}')

def parse_transition(f):
    global nodes

    line = f.readline().split()
    _from, _to, _count = line[0], line[1], int(line[2])

    for node_name in [_from, _to]:
        if node_name in nodes:
            continue
        nodes[node_name] = Node(node_name)

    for i in range(_count):
        line = f.readline().split()
        symbol, stack, add = line[0], line[1], line[2]
        nodes[_from].add_transition(Transition(nodes[_from], nodes[_to], symbol, stack, add))


with open("input.txt") as f:
    nodes = {}
    lambda_symbol = f.readline()[:-1]
    initial_stack = f.readline()[:-1]
    initial_state = f.readline()[:-1]

    final_states = [fs for fs in f.readline().split()]

    for i in range(int(f.readline())):
        parse_transition(f)
    words = [f.readline()[:-1] for i in range(int(f.readline()))]

for node in nodes.values():
    print(node)

npda = NPDA(nodes, nodes[initial_state], lambda_symbol, initial_stack)
for word in words:
    npda.check(word)
