from networkx import MultiDiGraph
import osmnx as ox


class Location:
    def __init__(self, name : str, lat: float, long: float):
        self.name = name
        self.lat = lat
        self.long = long
    
    def to_node(self, graph : MultiDiGraph):
        return ox.distance.nearest_nodes(graph, self.long, self.lat)
