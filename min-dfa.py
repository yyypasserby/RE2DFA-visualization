import generateRE
import re2nfa as r2n
import nfa2dfa as n2d
from collections import deque
import networkx as nx

def isInSameSets(a, b, list_sets):
    for m_set in list_sets:
        if a in m_set and b in m_set:
            return True
    return False

def checkTerminals(list_sets, transition_table, terminal):
    old_length = 0
    list_sets2 = []
    while True:
        length_old = len(list_sets)
        for m_set in list_sets:
            if len(m_set) <= 1:
                list_sets2.append(m_set)
                continue
            next_set = {}
            for item in m_set:
                next_node = transition_table[item][terminal]
                for traversal_set in list_sets:
                    if next_node in traversal_set:
                        if not next_set.has_key(frozenset(traversal_set)):
                            next_set[frozenset(traversal_set)] = [item]
                        else:
                            next_set[frozenset(traversal_set)].append(item)
            for item in next_set.itervalues():
                list_sets2.append(set(item))
        if length_old == len(list_sets2):
            list_sets = list_sets2
            break
        else:
            list_sets = list_sets2
            list_sets2 = []
    return list_sets

def checkForDivision(list_sets, transition_table, terminals):
    for terminal in terminals:
        list_sets = checkTerminals(list_sets, transition_table, terminal)
        print list_sets, terminal
    return list_sets

def toBeCombined(rules, list_sets):
    for sets in list_sets:
        if rules in sets:
            return sets
    raise Exception('Not such rules in list_sets')

def drawMinDFA(min_transition_table, list_sets):
    reverse = {}
    cnt = 0
    for sets in list_sets:
        if set([]) in sets:
            continue
        reverse[frozenset(sets)] = cnt
        cnt += 1

    g = nx.MultiDiGraph()
    for rule in min_transition_table:
        if set([]) in rule:
            continue
        for trans in min_transition_table[rule]:
            print rule
            print trans
            print min_transition_table[rule][trans]
            if set([]) in min_transition_table[rule][trans]:
                continue
            else:
                g.add_edge(reverse[frozenset(rule)], reverse[frozenset(min_transition_table[rule][trans])], label=trans)
    return g

def test():
    re = generateRE.generateRE()
    mg = r2n.convert(re)
    r2n.storeAsJPG(mg.graph, 'nfa')
    terminals = r2n.getAllTerminals(re)

    transition_table, all_states, acceptable_states = n2d.constructDFA(terminals, mg)
    dfa, reverse_table = n2d.showDFA(transition_table, all_states, acceptable_states)
    r2n.storeAsJPG(dfa, 'dfa')
    all_states = set(all_states)
    acceptable_states = set(acceptable_states)
    nonacceptable_states = all_states - acceptable_states
    list_sets = checkForDivision([acceptable_states, nonacceptable_states], transition_table, terminals)
    min_transition_table = {}
    for rules in transition_table:
        sets = toBeCombined(rules, list_sets)        
        min_transition_table[frozenset(sets)] = transition_table[rules]
    for rules in min_transition_table:
        for r in min_transition_table[rules]:
            sets = toBeCombined(min_transition_table[rules][r], list_sets)
            min_transition_table[rules][r] = sets
    for k,v in min_transition_table.items():
        print k, '|', v
    g = drawMinDFA(min_transition_table, list_sets)
    r2n.storeAsJPG(g, 'min_dfa');




if __name__ == '__main__':
    test()
