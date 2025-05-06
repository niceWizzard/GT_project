from utils.distance import get_distance
import networkx as nx
import pandas as pd
from utils.gen_alg import  GeneticAlgo
import matplotlib.pyplot as plt

Graph = nx.Graph()


df = pd.read_csv("calculations/pass_distances.csv")

locations =df["Loc1"].unique() 

for a in df.itertuples():
    Graph.add_edge(a.Loc1, a.Loc2, weight=a._4)
    

# nx.draw(Graph, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_weight="bold")
# plt.show()


route = GeneticAlgo(Graph, 100, 0.02    , 1000).run()

print(f"Route Distance: {route.length:.2f}m")


new_G = nx.Graph()

for i in range(len(route.cities)):
    nodeA = route.cities[i]
    nodeB = route.cities[(i+1)%len(route.cities)]
    new_G.add_edge(nodeA, nodeB, weight=get_distance(nodeA, nodeB))

pd.DataFrame(route.cities, columns=["Route"]).to_csv("calculations/gen_alg_sol.csv")

nx.draw(new_G, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_weight="bold")
plt.show()