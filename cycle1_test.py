import pytest
from cycle1 import has_cycle1, WeightedDiGraph
from testcases import parse_testcases
import networkx as nx
import random
import time

testcases = parse_testcases("testcases.txt")

def run_testcase(input:str):
    graph = WeightedDiGraph(*input)
    return has_cycle1(graph)
    

@pytest.mark.parametrize("testcase", testcases, ids=[testcase["name"] for testcase in testcases])
def test_cases(testcase):
    actual_output = run_testcase(testcase["input"])
    assert actual_output == testcase["output"], f"Expected {testcase['output']}, got {actual_output}"


def test_new_cases():
    # Basic cases
    assert not has_cycle1(WeightedDiGraph())
    assert not has_cycle1(WeightedDiGraph([0,1,2],[1,2,2]))
    assert has_cycle1(WeightedDiGraph([0,1,0.5],[1,2,0.5],[2,0,0.5]))

    # Edge cases
    assert not has_cycle1(WeightedDiGraph([0,1,1],[1,0,1]))
    assert has_cycle1(WeightedDiGraph([0,0,0.5]))
    assert not has_cycle1(WeightedDiGraph([0,1,0.5]))

    # complex cases
    g = nx.DiGraph()
    g.add_edge(0,1,weight=2)
    g.add_edge(1,0,weight=2)
    g.add_edge(2,3,weight=0.5)
    g.add_edge(3,2,weight=0.5)
    assert has_cycle1(g)

    # Random cases
    for _ in range(15):
        n = random.randint(5, 10)
        g = nx.DiGraph()

        for u in range(n):
            for v in range(n):
                if u != v and random.random() < 0.3:
                    g.add_edge(u, v, weight=random.uniform(0.1, 2))

        result = has_cycle1(g)
        assert isinstance(result, bool)
    
    # cycle < 1
    g = nx.DiGraph()
    g.add_edge(0,1,weight=0.5)
    g.add_edge(1,2,weight=0.5)
    g.add_edge(2,0,weight=0.5)
    assert has_cycle1(g)

    # performance test
    n = 1000
    m = 100000

    g = nx.gnm_random_graph(n, m, directed=True)

    for u, v in g.edges():
        g[u][v]["weight"] = random.uniform(0.5, 2)

    start = time.time()
    result = has_cycle1(g)
    end = time.time()

    assert isinstance(result, bool)
    assert end - start < 1.0, f"Too slow: {end-start}"
