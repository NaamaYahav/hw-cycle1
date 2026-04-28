# import subprocess, sys
# subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx>=3.4"], stdout=subprocess.DEVNULL)

import networkx as nx, numpy as np

def WeightedDiGraph(*edges: list[tuple[int,int,float]])->nx.DiGraph:
    """
    A shorthand function for quickly generating a directed graph with weights on the edges

    >>> G = WeightedDiGraph([0,1,55],[1,2,66],[2,0,77])
    >>> G.edges[0,1]
    {'weight': 55}
    """
    return nx.DiGraph( [(u,v,{"weight":w}) for u,v,w in edges])
    

def has_cycle1(graph: nx.DiGraph)->bool:
    """
    return True iff the given graph has a directed cycle in which the product of weights is smaller than 1.

    >>> has_cycle1(WeightedDiGraph())    # empty graph
    False
    >>> has_cycle1(WeightedDiGraph([0,1,55],[1,2,66],[2,0,77]))
    False
    >>> has_cycle1(WeightedDiGraph([0,1,0.55],[1,2,0.66],[2,0,0.77]))
    True
    """
    # Your code here
    if not graph.nodes or not graph.edges:
        return False
    transformed = nx.DiGraph()

    for edge in graph.edges(data=True):
        u, v, attrs = edge
        w = attrs["weight"]
        
        transformed.add_edge(u, v, weight=np.log(w))

    return nx.negative_edge_cycle(transformed)



if __name__ == '__main__':
    # edges = eval(input())
    # graph = WeightedDiGraph(*edges)
    # print(has_cycle1(graph))
    import doctest
    print (doctest.testmod())
