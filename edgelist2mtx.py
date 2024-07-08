import networkx as nx
import scipy as sp
from datasets import files


if __name__ == "__main__":

    for f_path in files:
        g = nx.read_edgelist(f_path, create_using=nx.Graph if "undirected" in f_path else nx.DiGraph)
        m = nx.to_scipy_sparse_array(g)
        f_mtx = open(f_path.split(".txt")[0]+".mtx", "wb+")
        sp.io.mmwrite(f_mtx, m)
