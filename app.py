import flask as fl
import pandas as pd
import math
import copy
import time

app = fl.Flask(__name__)
app.secret_key = 'secret_key'

def pr_key(e):
    return e[0]

class PageRank:
    def compute_out_weights(self, graph, n_node):
        out_weights = [0 for i in range(n_node)]
        for i in range(n_node):
            outgoing_weight = 0
            for j in range(n_node):
                outgoing_weight += int(math.ceil(graph[j][i]))
            out_weights[i] = outgoing_weight
        return out_weights

    def update_value(self, node_idx, graph,
                     n_node, old_values, damp_term, out_weights,
                     damp_factor):
        new_value = damp_term
        page_rank_sum = 0
        for other_node_idx in range(n_node):
            if other_node_idx == node_idx:
                continue
            if math.ceil(graph[node_idx][other_node_idx] > 0):
                page_rank_sum += old_values[other_node_idx] / out_weights[other_node_idx]
        result = new_value + damp_factor * page_rank_sum
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
            old_values = pr.copy()
            for node_idx in range(n_node):
                pr[node_idx] = self.update_value(
                                            node_idx, graph, n_node, old_values,
                                            damp_term, out_weights,
                                            damp_factor)
        value_name = [(pr[i], names[i]) for i in range(n_node)]
        value_name.sort(key=pr_key, reverse=True)
        str_list = [x[1] + ": " + str(round(x[0], 7)) for x in value_name][:n_res]
        print(sum(pr))
        end = time.time()
        return str_list, round(end - start, 2)

class Hits:
    def run(self, graph, names):
        return [f"Ran Hits"], 0


class Discovery:
    def run(self, graph, names):
        return [f"Ran Discovery"], 0

class Output:
    def __init__(self, pagerank, hits, discovery):
        self.data = ""
        self.pagerank = pagerank
        self.hits = hits
        self.discovery = discovery

    def read_df(self, file_name):
        df = None
        if file_name == "Facebook":
            df = pd.read_csv("datasets/facebook.csv")
        elif file_name == "Instagram":
            df = pd.read_csv("datasets/instagram.csv")
        elif file_name == "Twitter":
            df = pd.read_csv("datasets/twitter.csv")
        return df

    def df_to_graph(self, as_list):
        graph = list(map(lambda x:x[1:], as_list))
        graph = [list( map(int,i) ) for i in graph]
        return graph

    def extract_names(self, df):
        names = df.columns.tolist()[1:]
        names = list(map(lambda x: x.replace(u'\xa0', u'').strip(), names))
        return names

    def update(self, selected_algo, selected_dataset):
        df = self.read_df(selected_dataset)
        as_list = df.values.tolist()
        graph = self.df_to_graph(as_list)
        names = self.extract_names(df)
        if selected_algo == "PageRank":
            self.data, time = self.pagerank.run(graph, names)
            print(f"PageRank took {time} seconds")
        elif selected_algo == "HITS":
            self.data, time = self.hits.run(graph, names)
        elif selected_algo == "Community discovery":
            self.data, time = self.discovery.run(graph, names)

pagerank = PageRank()
hits = Hits()
discovery = Discovery()
output = Output(pagerank, hits, discovery)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'selected_algo' not in fl.session:
        fl.session['selected_algo'] = ''
    if 'selected_dataset' not in fl.session:
        fl.session['selected_dataset'] = ''
    if fl.request.method == 'POST':
        selected_algo = fl.request.form['selected_algo']
        selected_dataset = fl.request.form['selected_dataset']
        fl.session['selected_algo'] = selected_algo
        fl.session['selected_dataset'] = selected_dataset
        output.update(selected_algo, selected_dataset)
    selected_algo = fl.session.get('selected_algo', '')
    selected_dataset = fl.session.get('selected_dataset', '')
    return fl.render_template("index.html", selected_algo=selected_algo,
                              selected_dataset=selected_dataset,
                              output=output.data)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
