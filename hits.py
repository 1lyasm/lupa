import networkx as nx
import numpy as np
import time as time
from sknetwork.visualization import svg_graph
import scipy as scipy

def hits_key(e):
    return e[1]

class Hits:
    def run(self, graph, names):
        start = time.time()
        n_res = 10
        g = nx.from_numpy_array(np.array(graph))
        h, a = nx.hits(g)
        hubs = [(names[idx], val) for idx, val in h.items()]
        auths = [(names[idx], val) for idx, val in a.items()]
        hubs.sort(key=hits_key, reverse=True)
        auths.sort(key=hits_key, reverse=True)
        str_list = ["Hubs:", ""]
        str_list.extend([v[0] + ": " + str(round(v[1], 7)) for v in hubs][:n_res])
        str_list.extend(["", "Authorities:", ""])
        str_list.extend([v[0] + ": " + str(round(v[1], 7)) 
                            for v in auths][:n_res])
        image = svg_graph(scipy.sparse.csr_matrix(graph),
                          scores=a, width=1200, height=1000)
        end = time.time()
        return str_list, round(end - start, 2), image
