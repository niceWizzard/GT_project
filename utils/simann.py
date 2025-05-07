import networkx as nx
import random 
from functools import cache
import numpy as np


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
        