import networkx as nx
import random 
from functools import cache
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from utils.distance import get_distance


def simulated_annealing(G: nx.Graph, temperature: float, alpha: float, iterations: int) -> tuple[tuple, float]:

    nodes = list(G.nodes)
    distances = {u: {v: G[u][v]['weight'] for v in G[u] if u != v} for u in nodes}
    @cache
    def get_length(tour: tuple) -> float:
        tour_size = len(tour)
        return sum(
            distances[tour[i]][tour[(i+1) % tour_size]] for i in range(tour_size)
        ) 
    
    @cache
    def get_neighbors(tour: tuple):
        neighbors: list[tuple] = []
        for i in range(len(tour)):
            for j in range(i + 1, len(tour)):
                neighbor = list(tour)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(tuple(neighbor))
        return neighbors

    current_tour = tuple(random.sample(nodes, len(nodes)))
    current_distance = get_length(current_tour)
    best_tour = current_tour
    best_distance = current_distance

    for _ in range(iterations):
        neighbors = get_neighbors(current_tour)
        next_tour = random.choice(neighbors)
        next_distance = get_length(next_tour)

        if next_distance < current_distance or random.random() < np.exp((current_distance - next_distance) / temperature):
            current_tour, current_distance = next_tour, next_distance

            if current_distance < best_distance:
                best_tour, best_distance = current_tour, current_distance

        temperature *= alpha

    return best_tour, best_distance
        


Graph = nx.Graph()

df = pd.read_csv("calculations/pass_distances.csv")

locations =df["Loc1"].unique() 

for a in df.itertuples():
    Graph.add_edge(a.Loc1, a.Loc2, weight=a._4)
    
start = time.time()
tour, distance = simulated_annealing(Graph, 10_000, 0.995,20_000)
print(f"Finished: {(time.time() - start):.5f}s | Distance: {distance:.5f}m")


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

print("Saving file to SIM_ANN.html...")
m.save("calculations/SIM_ANN.html")