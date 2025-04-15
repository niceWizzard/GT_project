from location import Location
import osmnx as ox
import networkx as nx
import folium

from location_graph import LocationGraph

hospitals = [
    Location("ACE Malolos Doctors", 14.853554735231283, 120.81142465744408,),
    Location("Bulacan Medical Center/Hospital(BMC)", 14.858302418099049, 120.81745447386649,),
]

schools = [
    Location("Lab High", 14.85892925424361, 120.81368878373229),
    Location("PCCAM High", 14.866952161816126, 120.82409019218207)
]

place_name = "Malolos, Bulacan, Philippines"
locationGraph = LocationGraph(place_name)
edges = ox.graph_to_gdfs(locationGraph.G, nodes=False)

print("Doing...")

for school in schools:
    print(f"Calculating {school.name}")
    m = folium.Map(location=[school.lat, school.long], zoom_start=15)
    # Add the road network to the map
    for _, edge in edges.iterrows():
        points = [(lat, lon) for lon, lat in edge["geometry"].coords]
        folium.PolyLine(points, color="gray", weight=3).add_to(m)
    closest,distance = locationGraph.get_closest(school, hospitals)
    print(f"{school.name} is closer with {closest.name} with distance: {distance}m")
    print("Saving to file...")
    path = nx.shortest_path(locationGraph.G, school.to_node(locationGraph.G), closest.to_node(locationGraph.G), weight="length")
    path_coords = [(locationGraph.G.nodes[node]['y'], locationGraph.G.nodes[node]['x']) for node in path]
    folium.PolyLine(path_coords, color="red", weight=5).add_to(m)

    folium.Marker([school.lat, school.long], popup="Start", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker([closest.lat, closest.long], popup="End", icon=folium.Icon(color="red")).add_to(m)

    for node, data in locationGraph.G.nodes(data=True):
        folium.CircleMarker(
            location=(data['y'], data['x']),  # Node coordinates
            radius=2,  # Adjust node size
            color="black",  # Node border color
            fill=True,
            fill_color="black",  # Node fill color
            fill_opacity=0.6  # Transparency
        ).add_to(m)


    m.save(f"calculations/{school.name}-closest.html")


print("FINISHED!")