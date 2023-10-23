import flask as fl

app = fl.Flask(__name__)
app.secret_key = 'secret_key'

class PageRank:
    def run(self, dataset):
        return f"Ran PageRank on {dataset}"

class Hits:
    def run(self, dataset):
        return f"Ran Hits on {dataset}"


class Discovery:
    def run(self, dataset):
        return f"Ran Discovery on {dataset}"

class Output:
    def __init__(self, pagerank, hits, discovery):
        self.data = ""
        self.pagerank = pagerank
        self.hits = hits
        self.discovery = discovery

    def update(self, selected_algo, selected_dataset):
        if selected_algo == "PageRank":
            self.data = self.pagerank.run(selected_dataset)
        elif selected_algo == "HITS":
            self.data = self.hits.run(selected_dataset)
        elif selected_algo == "Community discovery":
            self.data = self.discovery.run(selected_dataset)

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
