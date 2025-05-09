import pandas as pd
from geopy.distance import geodesic
import os
from data import locations_list, locations_count


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


results = []
visited = []
print("Calculating Distances")
for index, loc1 in enumerate(locations_list):
	for index2, loc2 in enumerate([loc2 for loc2 in locations_list if loc2.name != loc1.name]):
		if (loc1.name, loc2.name) in visited:
			continue
		print(f"{(index * (locations_count-1)) + index2+1}/{locations_count*(locations_count - 1)}")
		distance = geodesic((loc1.lat, loc1.long), (loc2.lat, loc2.long)).meters
		visited.append((loc1.name, loc2.name))
		visited.append((loc2.name, loc1.name))
		results.append(
			(loc1.name, loc2.name, distance)
		)

df = pd.DataFrame(results, columns=["Loc1", "Loc2", "Distance (m)"])
df.to_csv("calculations/pass_distances.csv")


print("FINISHED!")
print(df)