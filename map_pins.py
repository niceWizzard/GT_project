from data import locations_list
import folium


place_name = "Bulacan, Philippines"
print(f"Initializing Map of {place_name}...")

m = folium.Map(location=[locations_list[0].lat, locations_list[0].long], zoom_start=15)

for loc in locations_list:
    folium.Marker((loc.lat, loc.long)).add_to(m)


print("Saving file to PINS.html...")
m.save("calculations/LOC_PINS.html")