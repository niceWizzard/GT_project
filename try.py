from location import Location
import osmnx as ox
import networkx as nx
import folium
import pandas as pd
import os
from tqdm import tqdm
import time
from location_graph import LocationGraph

hospitals = [
    Location("ACE Malolos Doctors", 14.853554735231283, 120.81142465744408,),
    Location("Bulacan Medical Center Hospital(BMC)", 14.858302418099049, 120.81745447386649,),
    Location("Graman Medical Hospital Inc.", 14.84647720458458, 120.83460117593113,),
    Location("Malolos EENT Hospital", 14.8499986254405, 120.822678718528,),
    Location("Malolos Maternity Hospital", 14.8501139971557, 120.822242189016,),
    Location("Malolos San Ildefonso County Hospital", 14.8405069766113, 120.801353264675,),
    Location("Malolos San Vicente Hospital", 14.8457217693662, 120.817005823084,),
    Location("Mary Immaculate Maternity and General Hospital", 14.8377610194932, 120.813822697031,),
    Location("Melissa M. Juico, MD Clinic - Bulacan Provincial Hospital", 14.8569767364998, 120.814434194216,),
    Location("Ofelia L. Mendoza Maternity & General Hospital (Liang)", 14.8454236766064, 120.813091057165,),
    Location("Ofelia L. Mendoza Maternity & General Hospital (Mojon)", 14.8674632646949, 120.821274949354,),
    Location("Romel Cruz Hospital", 14.8110072325401, 120.842409630834,),
    Location("Sacred Heart Hospital of Malolos", 14.8515663584312, 120.817809870366,),
    Location("Santos General Hospital", 14.840886581182, 120.81171038819,),
    Location("St. Michael Clinic and Maternity Hospital", 14.8527404366392, 120.816038676889,),
    Location("Stma Trinidad Hospital", 14.871006333866, 120.821389699214,)
]

schools = [
    Location("Lab High", 14.85892925424361, 120.81368878373229),
    Location("PCCAM High", 14.866952161816126, 120.82409019218207),
    Location("Barasoain Memorial Integrated School", 14.857600402504747, 120.817597896389,),
    Location("Bulacan Ecumenical School", 14.84796803241317, 120.814851991366,),
    Location("Bulacan Polythecnic College", 14.866813328498182, 120.806651822875,),
    Location("Bulacan State University", 14.857909024618733, 120.814264396364,),
    Location("Caingin E.S", 14.844145629656976, 120.804476703794,),
    Location("Calero E.S", 14.830118014377561, 120.811337091079,),
    Location("Caniogan E.S", 14.846107850740472, 120.817004889494,),
    Location("Catmon Elementary School CMIS Catmon", 14.85086166, 120.813230705372,),
    Location("Centro Escolar Integrated School", 14.870182671698426, 120.800546627749,),
    Location("Centro Escolar University", 14.870742327593709, 120.801832697842,),
    Location("CMIS Atlag", 14.829528675433416, 120.820444777527,),
    Location("CMIS Sto. Rosario", 14.839058831526806, 120.813625509482,),
    Location("Gen. Isidro Torres Memorial E.S", 14.816258551941608, 120.837320153981,),
    Location("Harvesters Missions International School", 14.874154600562086, 120.787571014243,),
    Location("Holy Spirit Academy of Mal.", 14.843302416944978, 120.835835842758,),
    Location("Immaculate Conception School of Mal.", 14.842511310556228, 120.812262799036,),
    Location("La Consolacion University Philippines (Barasoain Campus)", 14.846621658413243, 120.813192537857,),
    Location("La Consolacion University Philippines (Main Campus)", 14.853410752219135, 120.813197544064,),
    Location("Ma. Therese Montessori School", 14.854598839780904, 120.811885518226,),
    Location("Mabolo E.S", 14.84221606321911, 120.825833542512,),
    Location("Malolos Adventis E.S", 14.840226412056285, 120.811110498219,),
    Location("Malolos Christian School", 14.830801114971333, 120.820054530169,),
    Location("Mary the Queen School of Mal.", 14.840866179535857, 120.812202542583,),
    Location("Marcelo H. del Pilar Nat. HS", 14.841401294342612, 120.838533092263,),
    Location("Montessori School of Malolos(Preschool)",	14.8442038075082, 120.812384391099,),
    Location("Pasahan E.S",	14.821947859942494, 120.827009147036,),
    Location("San Agustin Elementary School", 14.84810609, 120.809488865122,),
    Location("San Juan E.S", 14.83433278163832, 120.814804115585,),
    Location("St. Joseph Parochial School",	14.821576430109518, 120.827592335552,),
    Location("Stella Maris Academy of Mal.", 14.853389180639471, 120.811143899941,),
    Location("STI College Malolos",14.84791238370636, 120.828720236995,),
    Location("Sto. Cristo E.S", 14.829458150206746, 120.81757520484,),
    Location("Tikay E.S", 14.84050757746236, 120.853773395145,)
]

place_name = "Malolos, Bulacan, Philippines"
locationGraph = LocationGraph(place_name)
edges = ox.graph_to_gdfs(locationGraph.G, nodes=False)


calc_data = []

directory_name = "calculations"

try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

colors = ["blue", "green", "purple", "orange", "darkred", "lightblue", "darkgreen", "cadetblue", "pink"]
marker_colors = ["green", "blue", "purple", "orange", "darkgreen"]

m = folium.Map(location=[schools[0].lat, schools[0].long], zoom_start=15)

for node, data in locationGraph.G.nodes(data=True):
        folium.CircleMarker(
            location=(data['y'], data['x']),  # Node coordinates
            radius=2,  # Adjust node size
            color="black",  # Node border color
            fill=True,
            fill_color="black",  # Node fill color
            fill_opacity=0.6  # Transparency
        ).add_to(m)

for _, edge in edges.iterrows():
        points = [(lat, lon) for lon, lat in edge["geometry"].coords]
        folium.PolyLine(points, color="gray", weight=3).add_to(m)

pbar = tqdm(schools, ncols=60)
for index,school in enumerate(pbar):
    (f"Calculating {school.name}")
    closest,distance,path = locationGraph.get_closest(school, hospitals)
    calc_data.append((school.name, closest.name, distance))
    # print("Saving to file...")
    color = colors[index % len(colors)]
    path_coords = [(locationGraph.G.nodes[node]['y'], locationGraph.G.nodes[node]['x']) for node in path]
    folium.PolyLine(path_coords, color=color, weight=5, popup=f"{school.name}-{closest.name}").add_to(m)

    folium.Marker([school.lat, school.long], popup=f"{school.name}", icon=folium.Icon(color=color)).add_to(m)
    folium.Marker([closest.lat, closest.long], popup=closest.name, icon=folium.Icon(color="red")).add_to(m)

    
pd.DataFrame(data=calc_data, columns=["School", "Closest Hospital", "Distance"]).to_csv("./calculations/data.csv")
print("Saving file to PATHS.html...")
m.save("PATHS.html")

print(pd.DataFrame(data=calc_data, columns=["School", "Closest Hospital", "Distance"]))

print("FINISHED!")