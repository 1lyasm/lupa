from cdlib import algorithms
import networkx as nx
import numpy as np
import time as time

class Discovery:
    def run_algo(self, str_list, g, names, n_node_shown, algo):
        communities = algo(g)
        avg_dists = [round(x, 4) for x in communities.avg_distance(summary=False)]
        sizes = communities.size(summary=False)
        node_comm = communities.to_node_community_map()
        max_comm = max(list(node_comm.values()))[0]
        comms = [[] for i in range(max_comm + 1)]
        for i in range(max_comm + 1):
            for key, value in node_comm.items():
                for j in value:
                    comms[j].append(key)
        str_list.extend([f"""Community {i} (node count: {sizes[i]},
                    avg path length: {avg_dists[i]}):
                    {', '.join(names[x] for x in comms[i][0:n_node_shown])}"""
                    for i in range(max_comm + 1)])
        return communities

    def run(self, graph, names):
        start = time.time()
        n_node_shown = 12
        str_list = [f"""Output of Louvain algorithm
                    (showing only top {n_node_shown} results):""", ""]
        g = nx.from_numpy_array(np.array(graph))
        louvain_comms = self.run_algo(str_list, g, names,
                                      n_node_shown, algorithms.louvain)
        str_list.extend(["", "Output of Leiden algorithm:", ""])
        leiden_comms = self.run_algo(str_list, g, names,
                                     n_node_shown, algorithms.leiden)
        nmi_score = louvain_comms. \
            normalized_mutual_information(leiden_comms).score
        str_list.extend(["", f"""NMI score between Louvain and Leiden
                         algorithm outputs: {round(nmi_score, 4)}"""])

        end = time.time()
        return str_list, round(end - start, 2)
