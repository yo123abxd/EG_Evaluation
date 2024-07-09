import networkx as nx
import nx_cugraph as nxcg
from benchmark import benchmark
import numpy as np
from glob import glob
from datasets import files, files_BC, files_Dijkstra, files_k_core

if __name__ == "__main__":
    for f in files:
        print(f"EasyGraph curr file: {f}")

        print("Profiling loading", flush=True)
        print("========================================")

        g=None

        if "undirected" in f:
            benchmark('nxcg.from_networkx(nx.read_edgelist(f, create_using=nx.Graph))', globals=globals(), n=5)
            g = nx.read_edgelist(f, create_using=nx.Graph)
        else:
            #directed
            benchmark('nxcg.from_networkx(nx.read_edgelist(f, create_using=nx.DiGraph))', globals=globals(), n=5)
            g = nx.read_edgelist(f, create_using=nx.DiGraph)

        g.remove_edges_from(nx.selfloop_edges(g))
        eg_g_nodes = list(g.nodes())
        g=nxcg.from_networkx(g)


        if f.split("/")[-1] in files_BC:
            print(f"Profiling betweenness centrality f: {f}", flush=True)
            print("========================================")

            benchmark('nx.betweenness_centrality(g)', globals=globals(), n=5)



        if f.split("/")[-1] in files_Dijkstra:
            print(f"Profiling SSSP f: {f}", flush=True)
            print("========================================")

            # shortest_path_length(G, source=None, target=None, weight=None, method='dijkstra')
            # the nx won't calculate shortest_path_length unless converted to dict
            benchmark('dict(nx.shortest_path_length(g))', globals=globals(), n=5)



        if f.split("/")[-1] in files_k_core:
            print(f"Profiling k_core f: {f}", flush=True)
            print("========================================")

            g = nx.read_edgelist(f, create_using=nx.Graph)
            g.remove_edges_from(nx.selfloop_edges(g))
            g = nxcg.from_networkx(g)
            benchmark('nx.core_number(g)', globals=globals(), n=100)

        