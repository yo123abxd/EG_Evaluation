import networkx as nx
import nx_cugraph as nxcg
from benchmark import benchmark
import numpy as np
from glob import glob

if __name__ == "__main__":
    directed_filedir  = "datasets/directed"
    undirected_filedir  = "datasets/undirected"
    n = 5

    files = glob(f"{directed_filedir}/*") + glob(f"{undirected_filedir}/*")

    for f in files:
        print(f"EasyGraph curr file: {f}")

        print("Profiling loading")
        print("========================================")

        g=None

        if "undirected" in f:
            benchmark('nxcg.from_networkx(nx.read_edgelist(f, create_using=nx.Graph))', globals=globals(), n=n)
            g = nx.read_edgelist(f, create_using=nx.Graph)
        else:
            #directed
            benchmark('nxcg.from_networkx(nx.read_edgelist(f, create_using=nx.DiGraph))', globals=globals(), n=n)
            g = nx.read_edgelist(f, create_using=nx.DiGraph)

        eg_g_nodes = list(g.nodes())
        g=nxcg.from_networkx(g)


        print("Profiling betweenness centrality")
        print("========================================")

        benchmark('nx.betweenness_centrality(g)', globals=globals(), n=n)



        print("Profiling SSSP")
        print("========================================")

        # shortest_path_length(G, source=None, target=None, weight=None, method='dijkstra')
        # the nx won't calculate shortest_path_length unless converted to dict
        benchmark('dict(nx.shortest_path_length(g))', globals=globals(), n=n)



        print("Profiling k_core")
        print("========================================")

        g = nxcg.from_networkx(nx.read_edgelist(f, create_using=nx.Graph))
        benchmark('nx.core_number(g)', globals=globals(), n=n)

        