import networkx as nx
import os
import sys
import re2nfa as r2n
import nfa2dfa as n2d
import min_dfa 
import io

def storeAsJPG(mg, name='nfa', openow=False):
    nx.write_dot(mg, name + '.dot')
    os.system('dot -Tjpg ' + name + '.dot -o ' + name + '.jpg')
    if openow:
        os.system('open ' + name + '.jpg')

def generateThreeFA(re, name):
    nfa = r2n.re2nfa(re)
    storeAsJPG(nfa.graph, name + 'nfa')
    terminals = r2n.getAllTerminals(re)

    transition_table, all_states, acceptable_states = n2d.constructTransitionTable(terminals, nfa)
    dfa, reverse_table = n2d.constructDFA(transition_table, all_states, acceptable_states)
    storeAsJPG(dfa.graph, name + 'dfa')

    mindfa, min_reverse_table = min_dfa.constructMinDFA(transition_table, all_states, dfa.first, dfa.last, terminals)
    storeAsJPG(mindfa.graph, name + 'min_dfa');



class MyGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.first = -1
        self.last  = -1

    def __str__(self):
        return str(self.first) + '--' + str(self.graph[self.first]) + '--' + str(self.last)




