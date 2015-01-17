import networkx as nx
import os

def storeAsJPG(mg, name='nfa', openow=False):
    nx.draw_graphviz(mg)
    nx.write_dot(mg, name + '.dot')
    os.system('dot -Tjpg ' + name + '.dot -o ' + name + '.jpg')
    if openow:
        os.system('open ' + name + '.jpg')

class MyGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.first = -1
        self.last  = -1

    def __str__(self):
        return str(self.first) + '--' + str(self.graph[self.first]) + '--' + str(self.last)




