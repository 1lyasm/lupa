import flask as fl
import pandas as pd
from pr import PageRank, pr_key
from hits import Hits
from disc import Discovery

app = fl.Flask(__name__)
app.secret_key = 'secret_key'

class Output:
    def __init__(self, pr, hits, discovery):
        self.data = ""
        self.pr = pr
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
            self.data, time = self.pr.run(graph, names)
            print(f"pr took {time} seconds")
        elif selected_algo == "HITS":
            self.data, time = self.hits.run(graph, names)
        elif selected_algo == "Community discovery":
            self.data, time = self.discovery.run(graph, names)

pr = PageRank()
hits = Hits()
discovery = Discovery()
output = Output(pr, hits, discovery)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'selected_algo' not in fl.session:
        fl.session['selected_algo'] = ''
    if 'selected_dataset' not in fl.session:
        fl.session['selected_dataset'] = ''
    if fl.request.method == 'POST':
        algo = fl.request.form['selected_algo']
        selected_dataset = fl.request.form['selected_dataset']
        fl.session['selected_algo'] = algo
        fl.session['selected_dataset'] = selected_dataset
        output.update(algo, selected_dataset)
    algo = fl.session.get('selected_algo', '')
    selected_dataset = fl.session.get('selected_dataset', '')
    return fl.render_template("index.html", selected_algo=algo,
                              selected_dataset=selected_dataset,
                              output=output.data)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
