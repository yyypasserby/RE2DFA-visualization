import networkx as nx
import os
import sys
import re2nfa as r2n
import nfa2dfa as n2d
import min_dfa 
import io

def storeAsJPG(mg, name='nfa', openow=False, filetype='jpg'):
    nx.write_dot(mg, name + '.dot')
    os.system('dot -T' + filetype + ' ' + name + '.dot -o ' + name + '.' + filetype)
    if openow:
        os.system('open ' + name + '.jpg')

def generateThreeFA(re, name, filetype='jpg'):
    nfa = r2n.re2nfa(re)
    storeAsJPG(nfa.graph, name + 'nfa', filetype=filetype)
    terminals = r2n.getAllTerminals(re)

    transition_table, all_states, acceptable_states = n2d.constructTransitionTable(terminals, nfa)
    dfa, reverse_table = n2d.constructDFA(transition_table, all_states, acceptable_states)
    storeAsJPG(dfa.graph, name + 'dfa', filetype=filetype)

    mindfa, min_reverse_table = min_dfa.constructMinDFA(transition_table, all_states, dfa.first, dfa.last, terminals)
    storeAsJPG(mindfa.graph, name + 'min_dfa', filetype=filetype)



class MyGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.first = -1
        self.last  = -1

    def __str__(self):
        return str(self.first) + '--' + str(self.graph[self.first]) + '--' + str(self.last)




