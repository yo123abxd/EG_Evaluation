import networkx as nx
import scipy as sp
from datasets import files, files_k_core


if __name__ == "__main__":

    for f_path in files:
        f_name = f_path.split(".txt")[0]
        directed = False if "undirected" in f_path else True
        if f_name+".txt" in files_k_core:
            directed = False

        g = nx.read_edgelist(f_path, create_using=nx.Graph if "undirected" in f_path else nx.DiGraph)
        m = nx.to_scipy_sparse_array(g)
        f_mtx = open(f_name+".mtx", "wb+")
        sp.io.mmwrite(f_mtx, m)
