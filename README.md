RE2DFA Visualization
==============================

A handy tool to visualize the process that converts Regular Expression (RE) to Nondeterministic Finite Automaton (NFA), Deterministic Finite Automaton (DFA) and Minimized Deterministic Finite Automaton (min-DFA).

## Requirements

- Graphviz
- Networkx
- matplotlib

## Purpose

- Deeper understanding of generating **NFA** & **DFA** & **min-DFA**
- Compare with the manual computation for correctness

## How to use

The tool is built with Python 2 and you need to install all the requirements above to run the project. [Networkx](http://networkx.github.io/) and [matplotlib](http://matplotlib.org/) can be installed by Python pip. [Graphviz](http://graphviz.org/), which is the graph-generator, can be installed with the help of [this page](http://graphviz.org/Download.php).

Then,

```bash
git clone git@github.com:yyypasserby/RE2DFA-visualization.git re2dfa
cd re2dfa && pip install -r requirements.txt

python judge.py
```

If you want to see the graph, 

```bash
python min_dfa.py
```

You can change the regular expression in the ```generateRE.py```.

## Some tips
This lib is not fully tested. Errors may occur.

### Support Regex:

- ()
- |
- *
- alphanumerics

