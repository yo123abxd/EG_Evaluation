import sys 
sys.path.append("..") 

import easygraph as eg
from benchmark import benchmark
import numpy as np
from glob import glob
from datasets import files, files_BC

if __name__ == "__main__":
    for f in files:
        if f.split("/")[-1] not in files_BC:
            continue

        print(f"EasyGraph curr file: {f}")

        g=eg.GraphC() if "undirected" in f else eg.DiGraphC()
        g.add_edges_from_file(f, weighted=False, is_transform=True)

        for warp_size in [1,2,4,8,16,32]:

            print(f"Profiling betweenness centrality f: {f} ; warp_size: {warp_size}", flush=True)
            print("========================================")

            benchmark(f'eg.betweenness_centrality(g, warp_size=warp_size)', globals=globals(), n=5)