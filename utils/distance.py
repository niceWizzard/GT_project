import pandas as pd

distances = {}

df = pd.read_csv("calculations/pass_distances.csv")

for i in df["Loc1"].unique():
    distances[i] = {}

for a in df.itertuples():
    distances[a.Loc1][a.Loc2] = a._4

def get_distance(loc1 : str, loc2: str) -> float:
    try:
        if loc1 in distances and loc2 in distances[loc1]:
            return distances[loc1][loc2]
        elif loc2 in distances and loc1 in distances[loc2]:
            return distances[loc2][loc1]
    except KeyError:
        raise ValueError(f"Invalid Location <{loc1}> and <{loc2}>")