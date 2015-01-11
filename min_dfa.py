import generateRE
import re2nfa as r2n
import nfa2dfa as n2d
from collections import deque
import networkx as nx
import public

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
    if len(terminals) == 0:
        return list_sets
    terminals = list(terminals)
    cnt = 0
    old_length = len(list_sets)
    while True:
        list_sets = checkTerminals(list_sets, transition_table, terminals[cnt])
        cnt += 1
        if len(list_sets) != old_length:
            cnt = 0
        old_length = len(list_sets)
        if cnt >= len(terminals):
            break
    return list_sets

def toBeCombined(rules, list_sets):
    for sets in list_sets:
        if rules in sets:
            return sets
    raise Exception('Not such rules in list_sets')

def isAcceptableStates(combinded_state, original_acceptable_states):
    for state in original_acceptable_states:
        if state in combinded_state:
            return True
    return False

def drawMinDFA(min_transition_table, begin_state, acceptable_states, list_sets):
    reverse = {}
    cnt = 0
    g = public.MyGraph()
    min_acceptable_states = []
    for sets in list_sets:
        if set([]) in sets:
            continue
        reverse[frozenset(sets)] = cnt
        if begin_state in sets:
            g.first = frozenset(sets)
        if isAcceptableStates(frozenset(sets), acceptable_states):
            g.graph.add_node(cnt, label='accept')
            min_acceptable_states.append(frozenset(sets))
        cnt += 1

    g.last = min_acceptable_states

    for rule in min_transition_table:
        if set([]) in rule:
            continue
        for trans in min_transition_table[rule]:
            if set([]) in min_transition_table[rule][trans]:
                continue
            else:
                g.graph.add_edge(reverse[frozenset(rule)], reverse[frozenset(min_transition_table[rule][trans])], label=trans)
    return g, reverse

def constructMinDFA(transition_table, all_states, begin_state, acceptable_states, terminals):
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
    return drawMinDFA(min_transition_table, begin_state, acceptable_states, list_sets)

def printTransitionTable(table):
    for rule in table:
        print rule, table[rule]

def test():
    re = generateRE.generateRE()
    nfa = r2n.re2nfa(re)
    public.storeAsJPG(nfa.graph, 'nfa')
    terminals = r2n.getAllTerminals(re)

    transition_table, all_states, acceptable_states = n2d.constructTransitionTable(terminals, nfa)
    dfa, reverse_table = n2d.constructDFA(transition_table, all_states, acceptable_states)
    public.storeAsJPG(dfa.graph, 'dfa')

    mindfa, min_reverse_table = constructMinDFA(transition_table, all_states, dfa.first, dfa.last, terminals)
    public.storeAsJPG(mindfa.graph, 'min_dfa');

if __name__ == '__main__':
    test()
