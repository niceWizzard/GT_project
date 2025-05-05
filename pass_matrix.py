
from location import Location
import folium
import pandas as pd
from location_graph import LocationGraph


colors = ["blue", "green", "purple", "orange", "darkred", "lightblue", "darkgreen", "cadetblue", "pink"]


locations = [
    Location("St John of God Parish San Rafael", 14.958225524337369, 120.96322267882005),
    Location("Old Municipal Building Baliwag", 14.95481604695801,120.90270723510771),
    Location("St Augustine Parish Baliwag", 14.955119055786852, 120.90061402905987),
    Location("St James the Apostle Parish Plaridel", 14.885810544266146, 120.85978010412184),
    Location("Simboryo Chapel of Quingua Plaridel", 14.884845717881191, 120.86089821685681),
    Location("Municipal Trial Court Pulilan", 14.90088287929189, 120.84847772733637, ),
    Location("Parish of St John the Baptist Calumpit", 14.916290963655934, 120.76871365675979),
    Location("Barasoain Church Malolos", 14.846298449087984, 120.81255809227919),
    Location("Immaculate Conception Parish Malolos", 14.842768314252513, 120.81144451558261),
    Location("Museum of Philippine Political History Malolos", 14.844310361974768, 120.81150852779331),
    Location("Malolos of Aguas Potables Malolos", 14.842713508543106, 120.81231003503166, ),
    Location("Hiyas Bulacan Cultural Center and Museum Malolos", 14.855007660211152 , 120.81458057949528),
]

results = []


place_name = "Bulacan, Philippines"
print(f"Initializing Map of {place_name}...")
locationGraph = LocationGraph(place_name)

m = folium.Map(location=[locations[0].lat, locations[0].long], zoom_start=15)

locations_count = len(locations)
print("Calculating Distances")
for index, loc1 in enumerate(locations):
    for index2, loc2 in enumerate([loc2 for loc2 in locations if loc2.name != loc1.name]):
        print(f"{(index * (locations_count-1)) + index2+1}/{locations_count*(locations_count - 1)}")
        path, distance = locationGraph.get_path(loc1, loc2)
        results.append(
            (loc1.name, loc2.name, distance)
        )

        color = colors[index % len(colors)]
        path_coords = [(locationGraph.G.nodes[node]['y'], locationGraph.G.nodes[node]['x']) for node in path]
        folium.PolyLine(path_coords, color=color, weight=5, popup=f"{loc1.name}-{loc2.name}").add_to(m)

        folium.Marker([loc1.lat, loc1.long], popup=f"{loc1.name}", icon=folium.Icon(color=color)).add_to(m)
        folium.Marker([loc2.lat, loc2.long], popup=loc2.name, icon=folium.Icon(color="red")).add_to(m)




df = pd.DataFrame(results, columns=["Loc1", "Loc2", "Distance (m)"])
df.to_csv("calculations/pass_distances.csv")
print("Saving file to PATHS.html...")
m.save("calculations/pass_paths.html")

print("FINISHED!")
print(df)