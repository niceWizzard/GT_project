import osmnx as ox
import networkx as nx

from location import Location


class LocationGraph:
    def __init__(self, place_name : str ):
        self.G = ox.graph_from_place(place_name, network_type="drive", simplify=False)
    
    def get_closest(self, orig : Location, destinations : list[Location]) -> tuple[Location, int]:
        closest = (100000, -1)
        orig_node = orig.to_node(self.G)
        for i,dest in enumerate(destinations):
            path_length = nx.shortest_path_length(self.G, orig_node, dest.to_node(self.G), weight="length")
            if path_length < closest[0]:
                closest = (path_length, i)
        if closest[1] == -1:
            return None
        return  (destinations[closest[1]], closest[0])