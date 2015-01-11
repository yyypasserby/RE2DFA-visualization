import min_dfa as mdfa
import re2nfa as r2n
import nfa2dfa as n2d
import public
import generateRE

def traversal_judge(min_dfa, reverse_table, string):
    state = reverse_table[min_dfa.first]
    fa = min_dfa.graph
    for char in string:
        found = False
        for nt in fa.successors_iter(state):
            for item in fa[state][nt].items():
                if char == item[1]['label']:
                    found = True
                    state = nt
                    break
            if found: break
        if not found:
            return False
    return True

def judge(re, string):
    nfa = r2n.re2nfa(re)
    terminals = r2n.getAllTerminals(re)

    transition_table, all_states, acceptable_states = n2d.constructTransitionTable(terminals, nfa)
    dfa, reverse_table = n2d.constructDFA(transition_table, all_states, acceptable_states)

    min_dfa, min_reverse_table = mdfa.constructMinDFA(transition_table, all_states, dfa.first, dfa.last, terminals)
    return traversal_judge(min_dfa, min_reverse_table, string)

def main():
    re = raw_input('Regular Expression: ')
    string = raw_input('String: ')

    result = judge(re, string)
    print 'True' if result else 'False'

if __name__ == '__main__':
    main()
