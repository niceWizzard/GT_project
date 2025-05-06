from data import locations
import folium


place_name = "Bulacan, Philippines"
print(f"Initializing Map of {place_name}...")

m = folium.Map(location=[locations[0].lat, locations[0].long], zoom_start=15)

for loc in locations:
    folium.Marker((loc.lat, loc.long)).add_to(m)


print("Saving file to PINS.html...")
m.save("calculations/LOC_PINS.html")