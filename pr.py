import time
import math
import copy

class PageRank:
    def compute_out_weights(self, graph, n_node):
        out_weights = [0 for i in range(n_node)]
        for i in range(n_node):
            out_wgt = 0
            for j in range(n_node):
                out_wgt += int(math.ceil(graph[j][i]))
            out_weights[i] = out_wgt
        return out_weights

    def update_val(self, node_idx, graph,
                     n_node, old_vals, damp_term, out_weights,
                     damp_factor):
        new_val = damp_term
        pr_sum = 0
        for other_node_idx in range(n_node):
            if other_node_idx == node_idx:
                continue
            if math.ceil(graph[node_idx][other_node_idx] > 0):
                pr_sum += old_vals[other_node_idx] / out_weights[other_node_idx]
        result = new_val + damp_factor * pr_sum
        return result

    def run(self, graph, names):
        start = time.time()
        n_iter = 10
        damp_factor = 0.85
        n_res = 10
        n_node = len(graph)
        damp_term = (1.0 - damp_factor) / n_node
        init_val = 1.0 / n_node
        pr = [init_val for i in range(n_node)]
        out_weights = self.compute_out_weights(graph, n_node)
        for i in range(n_iter):
            old_vals = pr.copy()
            for node_idx in range(n_node):
                pr[node_idx] = self.update_val(
                                            node_idx, graph, n_node, old_vals,
                                            damp_term, out_weights,
                                            damp_factor)
        val_name = [(pr[i], names[i]) for i in range(n_node)]
        val_name.sort(key=pr_key, reverse=True)
        str_list = [x[1] + ": " + str(round(x[0], 7)) for x in val_name][:n_res]
        print(sum(pr))
        end = time.time()
        return str_list, round(end - start, 2)

def pr_key(e):
    return e[0]
