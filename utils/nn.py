import networkx as nx


def nearest_neighbor(G : nx.Graph, start_index: int = 0) -> tuple[list[str], float]:
    nodes = list(G.nodes)
    n = len(nodes)
    first = nodes[start_index]

    #initialize route at the first node
    route = [first] 
    visited = {first}
    best_distance = 0
    while len(visited) < n: 
        current_node = route[-1]
        #Finds the nearest node to the current node that has not been visited yet
        nearest_node, distance = min([(i, G[current_node][i].get('weight')) for i in G[current_node] if i not in visited], key=lambda x: x[1])

        route.append(nearest_node)
        visited.add(nearest_node)
        best_distance += distance
    else:
        #Connect last node distance to the first node distance
        best_distance += G[current_node][first].get('weight')
    return (tuple(route), best_distance)