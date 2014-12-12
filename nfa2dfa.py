import re2nfa as r2n
import networkx as nx
from collections import deque
from generateRE import generateRE
import public

def findEpsilonClosure(node, mg):
    epsilon_closure = [node]
    traversal_q = deque()
    traversal_q.append(node)
    while len(traversal_q) != 0:
        t_node = traversal_q[0]
        for next_node in mg[t_node]:
            if mg[t_node][next_node][0]['label'] == 'epsilon':
                epsilon_closure.append(next_node)
                traversal_q.append(next_node)
        traversal_q.popleft()
    return set(epsilon_closure)

def findNextTerminalClosure(list_node, mg, terminal):
    new_add_nodes = []
    for node in list_node:
        for nn in mg[node]:
            if mg[node][nn][0]['label'] == terminal:
                new_add_nodes.append(nn)
    node_set = set(new_add_nodes)
    node_deque = deque(node_set)
    while len(node_deque) != 0:
        node = node_deque[0]
        ecl = findEpsilonClosure(node, mg)
        for t in ecl:
            if t not in node_set:
                node_deque.append(t)
                node_set.add(t)
        node_deque.popleft()
    return node_set

def constructTransitionTable(terminal_table, mg):
    all_sets = []
    acceptable_states = []
    transition_table = {}
    not_complete_sets = deque()
    first_set = findEpsilonClosure(mg.first, mg.graph)
    not_complete_sets.append(first_set)
    all_sets.append(frozenset(first_set))
    while len(not_complete_sets) != 0:
        t_set = not_complete_sets.popleft()
        if mg.last in t_set:
            acceptable_states.append(frozenset(t_set))
        t_dict = {}
        for terminal in terminal_table:
            ntc = findNextTerminalClosure(t_set, mg.graph, terminal)
            t_dict[terminal] = frozenset(ntc)
            if frozenset(ntc) not in all_sets:
                not_complete_sets.append(ntc.copy())
                all_sets.append(frozenset(ntc))
        transition_table[frozenset(t_set)] = t_dict

    return transition_table, all_sets, acceptable_states

def constructDFA(transition_table, all_sets, acceptable_states):
    reverse = {}
    cnt = 0
    for m_set in all_sets:
        reverse[m_set] = cnt
        cnt += 1
    g = nx.MultiDiGraph()
    for k,v in transition_table.items():
        f = reverse[k]
        for tran, next_set in v.items():
            g.add_edge(f, reverse[next_set], label=tran)
    for state in acceptable_states:
        g.node[reverse[state]]['label'] = 'accept'
    return g, reverse

def test():
    re = generateRE()
    terminal_table = r2n.getAllTerminals(re)
    print terminal_table
    mg = r2n.re2nfa(re)
    public.storeAsJPG(mg.graph)
    transition_table, all_sets, acceptable_states = constructTransitionTable(terminal_table, mg)
    print acceptable_states
    for t_set in all_sets:
        print t_set, transition_table[t_set] 

    mg, reverse = constructDFA(transition_table, all_sets, acceptable_states)
    public.storeAsJPG(mg, 'dfa')
        

if __name__ == '__main__':
    test()
