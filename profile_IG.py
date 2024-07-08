import igraph as ig
from benchmark import benchmark
import numpy as np
from glob import glob
from datasets import files, files_BC, files_Dijkstra, files_k_core

if __name__ == "__main__":
    n = 5

    for f in files:
        print(f"igraph curr file: {f}")

        print("Profiling loading", flush=True)
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

        if f in files_BC:
            print(f"Profiling betweenness centrality f: {f}", flush=True)
            print("========================================")

            benchmark('g.betweenness(directed=directed)', globals=globals(), n=n)


        if f in files_Dijkstra:
            print(f"Profiling SSSP f: {f}", flush=True)
            print("========================================")

            benchmark("g.distances(source = ig_g_nodes)", globals=globals(), n=n)

        if f in files_k_core:
            print(f"Profiling k_core f: {f}", flush=True)
            print("========================================")

            g = ig.Graph.Read_Edgelist(f,False)
            benchmark('g.coreness()', globals=globals(), n=n)

        