import igraph as ig
from benchmark import benchmark
import numpy as np
from glob import glob

if __name__ == "__main__":
    directed_filedir  = "datasets/directed"
    undirected_filedir  = "datasets/undirected"
    n = 5

    files = glob(f"{directed_filedir}/*") + glob(f"{undirected_filedir}/*")

    for f in files:
        print(f"igraph curr file: {f}")

        print("Profiling loading")
        print("========================================")

        g=None

        directed = False if "undirected" in f else True

        benchmark("ig.Graph.Read_Edgelist(f,directed)", globals=globals(), n=n)
        g = ig.Graph.Read_Edgelist(f,directed)


        g_node_set = set()
        for v1, v2 in g.get_edgelist():
            g_node_set.add(v1)
            g_node_set.add(v2)
        ig_g_nodes = list(g_node_set)

        print("Profiling betweenness centrality")
        print("========================================")

        benchmark('g.betweenness(directed=directed)', globals=globals(), n=n)


        print("Profiling SSSP")
        print("========================================")

        benchmark("g.distances(source = ig_g_nodes)", globals=globals(), n=n)

        print("Profiling k_core")
        print("========================================")

        g = ig.Graph.Read_Edgelist(f,False)
        benchmark('g.coreness()', globals=globals(), n=n)

        