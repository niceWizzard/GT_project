import networkx as nx
import random


# A route cities is acyclic. Length is cyclic, the distance from last node to first node is included.
class Route():
    def __init__(self, cities: list, length: float):
        self.cities = cities
        self.length = length
    
    def fitness(self) -> float:
        return 1/self.length
    
    def __eq__(self, value):
        if not isinstance(value, Route):
            return False
        return value.cities == self.cities

    def __str__(self):
        return f"Route: {self.cities} | Length: {self.length:.2f} | Fitness: {self.fitness():.4f}"
    def __repr__(self):
        return str(self)


class GeneticAlgo():
    def __repr__(self):
        return f"GeneticAlgo(route={self.best_route})"
    def __init__(self, G: nx.Graph, pop_size: int, mutation_rate: float, generations: int):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.G = G
        self.nodes = list(G.nodes)
        self.distances = {u: {v: G[u][v]['weight'] for v in G[u] if u != v} for u in G.nodes}
        self.best_route = None
        self.best_distance = float('Inf')
        self.num_cities = len(self.nodes)
        self.population: list[Route] = []
    
    def get_parent(self) -> Route:
        candidates = random.sample(self.population, 3)
        candidates.sort(key=lambda x : x.fitness(), reverse=True)
        return candidates[0]
    
    def mutate(self, route : Route):
        route = route.cities[:]
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.num_cities), 2)
            route[i], route[j] = route[j], route[i]
        return Route(route, self.get_route_length(route))
    
    def run(self) -> Route:
        self.population = self.gen_starting_population()
        for gen in range(self.generations):
            new_pop = []

            for _ in range(self.pop_size):
                parent1 = self.get_parent()
                parent2 = self.get_parent()
                while parent1 == parent2:
                    parent2 = self.get_parent()
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_pop.append(child)
            self.population = new_pop

            # Track best route
            current_best = min(self.population, key=lambda r: r.fitness())
            current_distance = current_best.length
            if current_distance < self.best_distance:
                self.best_route = current_best
                self.best_distance = current_distance
        return self.best_route

    def crossover(self, parent1: Route, parent2: Route):
        size = len(self.nodes)
        start, end = sorted(random.sample(range(size), 2))
        
        child = [None] * size
        # Step 1: Copy a slice from parent1
        child[start:end] = parent1.cities[start:end]

        # Step 2: Fill remaining from parent2
        p2_idx = 0
        for i in range(size):
            if child[i] is None:
                while parent2.cities[p2_idx] in child:
                    p2_idx += 1
                child[i] = parent2.cities[p2_idx]
        return Route(cities=child, length=self.get_route_length(child))
    
    def calculate_best_route(self) -> Route:
        return min(self.population, key=lambda x: x.fitness())

    def get_route_length(self, route: list[str]) -> float:
        return sum(
            self.distances[route[i]][route[(i+1) % len(route)]] for i in range(len(route))
        ) 

    def gen_starting_population(self) -> list[Route]:
        p = []
        for _ in range(self.pop_size):
            new_nodes = random.sample(self.nodes, len(self.nodes))
            length = self.get_route_length(new_nodes)
            p.append(
                Route(new_nodes, length)
            )
        return p




