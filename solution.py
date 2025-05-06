import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from gen_alg import Route, GeneticAlgo

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
    new_G.add_edge(route.cities[i], route.cities[(i+1)%len(route.cities)], weight=route.length)

nx.draw(new_G, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_weight="bold")
plt.show()