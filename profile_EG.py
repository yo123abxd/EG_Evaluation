import easygraph as eg
from benchmark import benchmark
import random
import numpy as np
from glob import glob

if __name__ == "__main__":
    directed_filedir  = "datasets/directed"
    undirected_filedir  = "datasets/undirected"
    n = 10

    files = glob(f"{directed_filedir}/*") + glob(f"{undirected_filedir}/*")

    for f in files:
        print(f"EasyGraph curr file: {f}")

        print("Profiling loading")
        print("========================================")

        g=None

        if "undirected" in f:
            benchmark('eg.GraphC().add_edges_from_file(f, weighted=False,is_transform=True)', globals=globals(), n=n)
            g=eg.GraphC()
            g.add_edges_from_file(f, weighted=False, is_transform=True)
        else:
            #directed
            benchmark('eg.DiGraphC().add_edges_from_file(f, weighted=False,is_transform=True)', globals=globals(), n=n)
            g=eg.DiGraphC()
            g.add_edges_from_file(f, weighted=False, is_transform=True)


        eg_g_nodes = list(g.nodes)

        print("Profiling betweenness centrality")
        print("========================================")

        benchmark('eg.betweenness_centrality(g)', globals=globals(), n=n)


        print("Profiling SSSP")
        print("========================================")

        benchmark('eg.multi_source_dijkstra(g, sources=eg_g_nodes)', globals=globals(), n=n)

        print("Profiling k_core")
        print("========================================")


        g=eg.GraphC()
        g.add_edges_from_file(f, weighted=False, is_transform=True)
        benchmark('eg.k_core(g)', globals=globals(), n=n)

        