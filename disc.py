from cdlib import algorithms
import networkx as nx
import numpy as np
import time as time

class Discovery:
    def run(self, graph, names):
        start = time.time()
        g = nx.from_numpy_array(np.array(graph))
        node_comm = algorithms.louvain(g, weight='weight',
            resolution=1., randomize=False).to_node_community_map()
        max_comm = max(list(node_comm.values()))[0]
        print(f"Discovery.run: max_comm: {max_comm}")
        comms = [[] for i in range(max_comm + 1)]
        for i in range(max_comm + 1):
            print(f"Discovert.run: i: {i}")
            for key, value in node_comm.items():
                for j in value:
                    comms[j].append(key)
        # print(f"comms: {comms}")
        # print(f"node_comm: {node_comm}")
        str_list = [f"""Community {i}:
                    {', '.join(names[x] for x in comms[i][0:len(comms[i]) - 1])}
                    {names[comms[i][len(comms) - 1]]}"""
                    for i in range(max_comm + 1)]
        str_list = [f"""Community {i}:
                {', '.join(names[x] for x in comms[i])}"""
                for i in range(max_comm + 1)]
    
        end = time.time()
        return str_list, round(end - start, 2)

        # start = time.time()
        # n_res = 10
        # g = nx.from_numpy_array(np.array(graph))
        # h, a = nx.hits(g)
        # hubs = [(names[idx], val) for idx, val in h.items()]
        # auths = [(names[idx], val) for idx, val in a.items()]
        # hubs.sort(key=hits_key, reverse=True)
        # auths.sort(key=hits_key, reverse=True)
        # str_list = [v[0] + ": " + str(round(v[1], 7)) for v in hubs][:n_res]
        # str_list.insert(0, "Hubs:")
        # str_list.append("")
        # str_list.append("Authorities:")
        # str_list.extend([v[0] + ": " + str(round(v[1], 7)) 
        #                     for v in auths][:n_res])
        # end = time.time()
        # return str_list, round(end - start, 2)

