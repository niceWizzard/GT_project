import networkx as nx
import pandas as pd
from utils.distance import get_distance
from utils.genalg import genetic_alg
import matplotlib.pyplot as plt
import time

Graph = nx.Graph()


df = pd.read_csv("calculations/pass_distances.csv")

locations =df["Loc1"].unique() 

for a in df.itertuples():
    Graph.add_edge(a.Loc1, a.Loc2, weight=a._4)
    

# nx.draw(Graph, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_weight="bold")
# plt.show()


start = time.time()
tour, distance = genetic_alg(Graph, 100, 0.05, 1000)
print(f"Finished: {time.time() - start} | Distance: {distance}")


new_G = nx.Graph()

for i in range(len(tour)):
    nodeA = tour[i]
    nodeB = tour[(i+1)%len(tour)]
    new_G.add_edge(nodeA, nodeB, weight=get_distance(nodeA, nodeB))

pd.DataFrame(tour, columns=["Route"]).to_csv("calculations/gen_alg_sol.csv")

nx.draw(new_G, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_weight="bold")
plt.show()