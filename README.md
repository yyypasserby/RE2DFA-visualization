Lexical Analysis Visualization
==============================

A visualization tools for process from re to nfa, dfa, min-dfa

##Requirements

- Graphviz
- Networkx
- matplotlib

##Usage

- Show the visualized graph to the user and make it more direct and easy to understand.

- a deeper understanding of generating **nfa** & **dfa** & **min-dfa**

- a homework for Compiler@SEU

##How to use

The project depends on python, you need to install all the requirements listed above. [Networkx](http://networkx.github.io/) and [matplotlib](http://matplotlib.org/) could be installed by python pip. [Graphviz](http://graphviz.org/) is a graph-generator, you could install it with the help of [this page](http://graphviz.org/Download.php).

Then,

```bash
git clone git@github.com:yyypasserby/lexical_analysis_visualization.git lex
cd lex
pip install -r requirements.txt

python judge.py
```

If you want to see the graph, 

```bash
python min_dfa.py
```

You could change the regular expression in the ```generateRE.py```.

##Some tips
This lib is not fully tested. Any errors may occur.

Supported regex:

- ()
- |
- *
- alphanumerics

