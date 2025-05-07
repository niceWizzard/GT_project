import networkx as nx
import time 
import pandas as pd
from utils.distance import get_distance
import matplotlib.pyplot as plt
import numpy as np

Graph = nx.Graph()


df = pd.read_csv("calculations/pass_distances.csv")


for a in df.itertuples():
    Graph.add_edge(a.Loc1, a.Loc2, weight=a._4)
    






new_G = nx.Graph()

for i in range(len(tour)):
    nodeA = tour[i]
    nodeB = tour[(i+1)%len(tour)]
    new_G.add_edge(nodeA, nodeB, weight=get_distance(nodeA, nodeB))

pd.DataFrame(tour, columns=["Route"]).to_csv("calculations/gen_alg_sol.csv")

nx.draw(new_G, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, font_weight="bold")
plt.show()


# Folium Version

import folium
from data import locations


place_name = "Bulacan, Philippines"
print(f"Initializing Map of {place_name}...")

m = folium.Map(location=[locations[0].lat, locations[0].long], zoom_start=15)

# Add marker to locations
for loc in locations:
    folium.Marker((loc.lat, loc.long)).add_to(m)

#Add edges 
for i in range(len(tour)):
    loc1 = tour[i]
    loc2 = tour[(i + 1) % len(tour)]

    loc1 = next((l for l in locations if l.name == loc1))
    loc2 = next((l for l in locations if l.name == loc2))
    folium.PolyLine([(loc1.lat, loc1.long), (loc2.lat, loc2.long)], color="blue", weight=5, opacity=0.8).add_to(m)

print("Saving file to NEAREST_N.html...")
m.save("calculations/NEAREST_N.html")

