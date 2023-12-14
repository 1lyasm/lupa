import flask as fl
import pandas as pd
import math
import copy
import time

app = fl.Flask(__name__)
app.secret_key = 'secret_key'

def page_rank_key(e):
    return e[0]

class PageRank:
    def compute_outgoing_weights(self, graph, node_count):
        outgoing_weights = [0 for i in range(node_count)]
        for i in range(node_count):
            outgoing_weight = 0
            for j in range(node_count):
                outgoing_weight += int(math.ceil(graph[j][i]))
            outgoing_weights[i] = outgoing_weight
        return outgoing_weights

    def update_value(self, node_index, graph,
                     node_count, old_values, damping_term, outgoing_weights,
                     damping_factor):
        new_value = damping_term
        page_rank_sum = 0
        for other_node_index in range(node_count):
            if other_node_index == node_index:
                continue
            if math.ceil(graph[node_index][other_node_index] > 0):
                page_rank_sum += old_values[other_node_index] / outgoing_weights[other_node_index]
        result = new_value + damping_factor * page_rank_sum
        return result

    def run(self, graph, names):
        start = time.time()

        iteration_count = 10
        damping_factor = 0.85
        result_count = 10

        node_count = len(graph)
        damping_term = (1.0 - damping_factor) / node_count
        initial_value = 1.0 / node_count
        page_rank_values = [initial_value for i in range(node_count)]
        outgoing_weights = self.compute_outgoing_weights(graph, node_count)

        for i in range(iteration_count):
            old_values = page_rank_values.copy()
            for node_index in range(node_count):
                page_rank_values[node_index] = self.update_value(
                                            node_index, graph, node_count, old_values,
                                            damping_term, outgoing_weights,
                                            damping_factor)
        value_name = [(page_rank_values[i], names[i]) for i in range(node_count)]
        value_name.sort(key=page_rank_key, reverse=True)
        string_list = [x[1] for x in value_name][:result_count]

        end = time.time()

        return string_list, round(end - start, 2)

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
            print(time)
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
