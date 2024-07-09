from glob import glob

directed_filedir  = "datasets/directed"
undirected_filedir  = "datasets/undirected"
files = glob(f"{directed_filedir}/*") + glob(f"{undirected_filedir}/*")


files_Dijkstra = set([
    "ER-10k.txt",
    "p2p-Gnutella08.txt",
    "wiki-Vote.txt",
    "ca-GrQc.txt",
    "ca-HepPh.txt",
    "ca-HepTh.txt",
])


files_k_core = set([
    "soc-Epinions1.txt",
    "amazon0601.txt",
    "email-EuAll.txt",
    "ER-100k.txt",
    "ER-500k.txt",
    "com-youtube.ungraph.txt",
])


files_BC = set([
    "ER-100k.txt",
    "ER-10k.txt",
    "soc-Epinions1.txt",
    "ca-CondMat.txt",
    "ca-HepPh.txt",
    "email-Enron.txt",
])
