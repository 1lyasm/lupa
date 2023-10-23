import math
from app import PageRank

graph = [[0, 0, 0, 0, 1],
         [0.5, 0, 0, 0, 0],
         [0.5, 0, 0, 0, 0],
         [0, 1, 0.5, 0, 0],
         [0, 0, 0.5, 1, 0]]
node_count = len(graph)
page_rank = PageRank()

print(page_rank.compute_outgoing_weights(graph, node_count))
print(page_rank.run(graph, []))

