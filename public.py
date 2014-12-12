import networkx as nx
import os

def storeAsJPG(mg, name='nfa'):
    nx.draw_graphviz(mg)
    nx.write_dot(mg, name + '.dot')
    os.system('dot -Tjpg ' + name + '.dot -o ' + name + '.jpg')
    os.system('open ' + name + '.jpg')


