import networkx as nx
import random 





def random_population(nodes: list, size: int):
    return [random.sample(nodes, len(nodes)) for _ in range(size)]



def genetic_alg(G: nx.Graph, pop_size: int, mutation_rate: float, generations: int) -> tuple[list, float]:
    # Initialize a random population
    nodes = list(G.nodes)
    distances = {u: {v: G[u][v]['weight'] for v in G[u] if u != v} for u in nodes}
    def crossover(parent1: list, parent2: list):
        size = len(nodes)
        start, end = sorted(random.sample(range(size), 2))
        
        child : list = [None] * size
        # Step 1: Copy a slice from parent1
        child[start:end] = parent1[start:end]

        # Step 2: Fill remaining from parent2
        p2_idx = 0
        for i in range(size):
            if child[i] is None:
                while parent2[p2_idx] in child:
                    p2_idx += 1
                child[i] = parent2[p2_idx]
        return child
    
    def mutate(route : list):
        route = route[:]
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(nodes)), 2)
            route[i], route[j] = route[j], route[i]
        return route
    
    def get_parent(population: list[list]) -> list:
        candidates = random.sample(population, 3)
        candidates.sort(key=lambda x : fitness(x), reverse=True)
        return candidates[0]

    def get_length(tour: list) -> float:
        tour_size = len(tour)
        return sum(
            distances[tour[i]][tour[(i+1) % len(tour)]] for i in range(len(tour))
        ) 

    def fitness(tour : list) -> float:
        return 1 / get_length(tour)

    population = random_population(nodes, pop_size)

    best_distance = float('Inf')
    best_tour = None

    for gen in range(generations):
        new_population: list[list] = []
        for _ in range(pop_size):
            p1 = get_parent(population)
            p2 = get_parent(population)
            while p1 == p2:
                p2 = get_parent(population)
            child = crossover(p1, p2)
            child = mutate(child)
            new_population.append(child)
        population = new_population
        current_best_tour = min(population, key=lambda r: fitness(r))
        current_best_distance = get_length(current_best_tour)
        if current_best_distance < best_distance:
            best_distance = current_best_distance
            best_tour = current_best_tour
    
    return best_tour, best_distance



