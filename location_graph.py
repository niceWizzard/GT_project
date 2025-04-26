import osmnx as ox
import networkx as nx

from location import Location


class LocationGraph:
    def __init__(self, place_name : str ):
        self.G = ox.graph_from_place(place_name, network_type="drive", simplify=False)
    
    def get_closest(self, orig: Location, destinations: list[Location]) -> tuple[Location, int, list[int]]:
        closest = (float('inf'), -1, [])  # (distance, index, path)
        orig_node = orig.to_node(self.G)
        
        for i, dest in enumerate(destinations):
            dest_node = dest.to_node(self.G)
            path = nx.shortest_path(self.G, orig_node, dest_node, weight="length")
            
            # Calculate path length manually by summing edge weights
            path_length = 0
            for u, v in zip(path[:-1], path[1:]):
                edge_data = self.G.get_edge_data(u, v)
                if isinstance(edge_data, dict):
                    # For MultiDiGraph (common in osmnx), pick the first edge
                    edge = edge_data[min(edge_data.keys())]
                    path_length += edge["length"]
                else:
                    path_length += edge_data["length"]

            if path_length < closest[0]:
                closest = (path_length, i, path)
        
        if closest[1] == -1:
            return None
        return (destinations[closest[1]], closest[0], closest[2])