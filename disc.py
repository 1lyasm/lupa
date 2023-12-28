from cdlib import algorithms
import networkx as nx
import numpy as np
import time as time

class Discovery:
    def run(self, graph, names):
        start = time.time()
        g = nx.from_numpy_array(np.array(graph))
        communities = algorithms.louvain(g, weight='weight',
            resolution=1., randomize=False)
        avg_dists = communities.avg_distance(summary=False)
        print(f"avg_dists: {avg_dists}")
        sizes = communities.size(summary=False)
        print(f"sizes: {sizes}")
        node_comm = communities.to_node_community_map()
        max_comm = max(list(node_comm.values()))[0]
        print(f"Discovery.run: max_comm: {max_comm}")
        comms = [[] for i in range(max_comm + 1)]
        for i in range(max_comm + 1):
            for key, value in node_comm.items():
                for j in value:
                    comms[j].append(key)
        str_list = [f"""Community {i} (node count: {sizes[i]}, avg path length: {avg_dists[i]}):
                    {', '.join(names[x] for x in comms[i][0:len(comms[i]) - 1])}
                    {names[comms[i][len(comms) - 1]]}"""
                    for i in range(max_comm + 1)]
    
        end = time.time()
        return str_list, round(end - start, 2)
