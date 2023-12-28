from cdlib import algorithms
import networkx as nx
import numpy as np
import time as time

class Discovery:
    def run(self, graph, names):
        start = time.time()
        g = nx.from_numpy_array(np.array(graph))
        louvain_communities = algorithms.louvain(g, randomize=False)
        leiden_communities = algorithms.leiden(g)
        avg_dists = [round(x, 4) for x in louvain_communities.avg_distance(summary=False)]
        print(f"avg_dists: {avg_dists}")
        sizes = louvain_communities.size(summary=False)
        print(f"sizes: {sizes}")
        nmi_score = louvain_communities. \
            normalized_mutual_information(leiden_communities).score
        print(f"nmi: {nmi_score}")
        node_comm = louvain_communities.to_node_community_map()
        max_comm = max(list(node_comm.values()))[0]
        print(f"Discovery.run: max_comm: {max_comm}")
        comms = [[] for i in range(max_comm + 1)]
        for i in range(max_comm + 1):
            for key, value in node_comm.items():
                for j in value:
                    comms[j].append(key)
        n_node_shown = 20
        str_list = [f"Top {n_node_shown} nodes in all comunities:"]
        str_list.extend([f"""Community {i}:
                    {', '.join(names[x] for x in comms[i][0:n_node_shown])}"""
                    for i in range(max_comm + 1)])
        str_list.extend([f"""Community {i} - node count: {sizes[i]},
                    avg path length: {avg_dists[i]}"""
                    for i in range(max_comm + 1)])
        str_list.extend([f"NMI score between Louvain and Leiden algorithm outputs: {nmi_score}"])

        end = time.time()
        return str_list, round(end - start, 2)
