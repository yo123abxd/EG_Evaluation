import easygraph as eg
from benchmark import benchmark
import numpy as np
from glob import glob
from datasets import files, files_BC, files_Dijkstra, files_k_core

if __name__ == "__main__":
    g=eg.GraphC()
    g.add_edges([(1,2)])
    eg.betweenness_centrality(g) # to mitigate the overhead of loading the shared library related to GPU functions
    for f in files:
        print(f"EasyGraph curr file: {f}")

        print("Profiling loading", flush=True)
        print("========================================")


        if "undirected" in f:
            benchmark('eg.GraphC().add_edges_from_file(f, weighted=False,is_transform=True)', globals=globals(), n=5)
            g=eg.GraphC()
            g.add_edges_from_file(f, weighted=False, is_transform=True)
        else:
            #directed
            benchmark('eg.DiGraphC().add_edges_from_file(f, weighted=False,is_transform=True)', globals=globals(), n=5)
            g=eg.DiGraphC()
            g.add_edges_from_file(f, weighted=False, is_transform=True)


        eg_g_nodes = list(g.nodes)

        if f.split("/")[-1] in files_BC:
            print(f"Profiling betweenness centrality f: {f}", flush=True)
            print("========================================")

            benchmark('eg.betweenness_centrality(g)', globals=globals(), n=5)


        if f.split("/")[-1] in files_Dijkstra:
            print(f"Profiling SSSP f: {f}", flush=True)
            print("========================================")

            benchmark('eg.multi_source_dijkstra(g, sources=eg_g_nodes)', globals=globals(), n=5)


        if f.split("/")[-1] in files_k_core:
            print(f"Profiling k_core f: {f}", flush=True)
            print("========================================")

            g=eg.GraphC()
            g.add_edges_from_file(f, weighted=False, is_transform=True)
            benchmark('eg.k_core(g)', globals=globals(), n=100)