import networkx as nx
import matplotlib
import os
from generateRE import generateRE
from collections import deque
import public

next_node = -1 
def nextNode():
    global next_node
    next_node += 1
    return next_node

class MyGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.first = -1
        self.last  = -1

def findParenthesis(string, pos):
    temp, i = -1, pos
    while i != len(string) and temp != 0:
        if string[i] == '(':
            temp -= 1
        if string[i] == ')':
            temp += 1
            if temp == 0:
                print string[pos : i]
                return i
        i += 1
    raise Exception("Could not find a corresponding parenthesis")

def convertTerminal2MG(terminal):
    mg = MyGraph()
    mg.first = nextNode()
    mg.last = nextNode()
    mg.graph.add_edge(mg.first, mg.last, label=terminal)
    return mg

def re2nfa(input_str):
    if len(input_str) == 0:
        return False
    mg_stack = []
    i, length = 0, len(input_str)
    while i < length:
        char = input_str[i]
        if isControlSymbol(char):
            if char == '(':
                pos = findParenthesis(input_str, i + 1)
                sub_mg = re2nfa(input_str[i + 1 : pos])
                mg_stack.append(sub_mg)
                i = pos + 1
            if char == '*':
                prev = mg_stack.pop()
                sub_mg = repeat(prev)
                mg_stack.append(prev)
                i += 1
            if char == '|':
                mg_stack.append(char)
                i += 1
        elif isTerminalSymbol(char):
            if len(mg_stack) != 0 and not mg_stack[-1] == '|':
                prev = mg_stack.pop()
                prev = concat(prev, convertTerminal2MG(char))
                mg_stack.append(prev)
            else:
                mg_stack.append(convertTerminal2MG(char))
            i += 1
    ret_mg = MyGraph()
    ret_mg.first, ret_mg.last = nextNode(), nextNode()
    ret_mg.graph.add_nodes_from([ret_mg.first, ret_mg.last])
    prev = None
    for now in mg_stack:
        if now == '|':
            union(ret_mg, prev)
            prev = None
        else:
            if prev is not None:
                prev = concat(prev, now)
            else:
                prev = now
    if prev is not None:
        union(ret_mg, prev)
    return ret_mg

def union(mg1, mg2):
    mg1.graph = nx.union(mg1.graph, mg2.graph)
    mg1.graph.add_edge(mg1.first, mg2.first, label='epsilon')
    mg1.graph.add_edge(mg2.last, mg1.last, label='epsilon')
    return mg1

def repeat(mg):
    mg.graph.add_edge(mg.last, mg.first, label='epsilon')
    return mg

def concat(mg1, mg2):
    mg1.graph = nx.union(mg1.graph, mg2.graph)
    mg1.graph.add_edge(mg1.last, mg2.first, label='epsilon')
    mg1.last  = mg2.last
    return mg1

def controlSymbols():
    return ['(', ')', '*', '|']

def isControlSymbol(char):
    return char in controlSymbols()

def isTerminalSymbol(char):
    return not char in controlSymbols()

def getAllTerminals(re):
    return set([char for char in re if isTerminalSymbol(char)])

def test():
    input_str = generateRE()
    mg = re2nfa(input_str)
    public.storeAsJPG(mg.graph)

if __name__ == '__main__':
    test()
