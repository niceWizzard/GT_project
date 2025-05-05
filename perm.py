import pandas as pd
import itertools

df = pd.read_csv("calculations/symmetric_distances.csv")

origin = df.loc[0, 'Loc1']

locations = {
    row['Loc2']: row['Average']
    for _, row in df.iterrows()
}

results = []

# Iterate through all 2-location combinations (excluding origin)
for loc1, loc2 in itertools.combinations(locations.keys(), 2):
    d1 = locations[loc1]
    d2 = locations[loc2]

    # Estimate third side using triangle inequality 
    est_min = abs(d1 - d2)
    est_max = d1 + d2

    valid = (d1 + est_min >= d2) and (d2 + est_min >= d1) and (d1 + d2 >= est_min)

    results.append({
        "Triplet": (origin, loc1, loc2),
        "Sides (m)": (round(d1, 2), round(d2, 2), f"{round(est_min, 2)}–{round(est_max, 2)}"),
        "Valid Triangle": valid
    })

for r in results:
    print(f"\nTriplet: {r['Triplet']}")
    print(f"Sides: A–B = {r['Sides (m)'][0]} m, A–C = {r['Sides (m)'][1]} m, B–C = {r['Sides (m)'][2]} m")
    print("Triangle Inequality Satisfied?" , "✅ Yes" if r["Valid Triangle"] else "❌ No")