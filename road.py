import time
import osmnx as ox
import networkx as nx
import pandas as pd
from typing import List, Tuple, Dict
from itertools import combinations, permutations
import multiprocessing as mp
from utils.location_graph import Location, LocationGraph
from data import locations_list

def process_location_pair(loc1: Location, loc2: Location, locGraph: LocationGraph) -> Tuple[str, str, Dict]:
    """
    Helper function to process a single pair of locations.  This is what each worker process will execute.
    """
    r1, d1 = locGraph.get_path(loc1, loc2)
    r2, d2 = locGraph.get_path(loc2, loc1)
    res = {
        "distance": max(d1, d2),
        "route": r1 if d1 > d2 else r2,
    }
    return loc1.name, loc2.name, res  # Return the names along with the result.

def calculate_distances_multithreaded(locations_list: List[Location], locGraph: LocationGraph) -> Dict[str, Dict[str, Dict]]:
    """
    Calculates shortest road distances between all pairs of locations using multiprocessing.

    Args:
        locations_list: List of Location objects.
        locGraph:  Pre-initialized LocationGraph object.

    Returns:
        A dictionary containing the results.
    """
    results = {loc.name: {} for loc in locations_list}
    comb = list(combinations(locations_list, 2))  # Convert to a list so it can be sliced.
    num_processes = mp.cpu_count()
    chunk_size = len(comb) // num_processes
    chunks = [comb[i:i + chunk_size] for i in range(0, len(comb), chunk_size)]


    with mp.Pool(processes=num_processes) as pool:
        # Prepare arguments for starmap
        tasks = [(loc1, loc2, locGraph) for chunk in chunks for loc1, loc2 in chunk]
        worker_results = pool.starmap(process_location_pair, tasks)

    # Organize the results.
    for loc1_name, loc2_name, res in worker_results:
        results[loc1_name][loc2_name] = res
        results[loc2_name][loc1_name] = res
    return results

def check_triangle_inequality(results: Dict[str, Dict[str, Dict]]):
    """
    Checks the triangle inequality for all triplets of locations.
    """
    print("Checking Triangle Inequality...")
    bad_triangles = [] # collect bad triangles instead of printing immediately
    for a_key, b_key, c_key in permutations(results.keys(), 3):
        ab = results[a_key][b_key]["distance"]
        bc = results[b_key][c_key]["distance"]
        ac = results[a_key][c_key]["distance"]
        s = ab + bc
        if s < ac - 1e-4:
            bad_triangles.append((a_key, b_key, c_key, ab, bc, ac))
    return bad_triangles

def save_results_to_csv(results: Dict[str, Dict[str, Dict]], filename="calculations/road_distances.csv"):
    """
    Saves the calculated distances to a CSV file.
    """
    out_res = []
    for a, b in combinations(results.keys(), 2):
        ab = results[a][b]["distance"]
        out_res.append((a, b, ab))
    print(f"Saving to {filename}")
    pd.DataFrame(out_res, columns=["Loc1", "Loc2", "Distances(m)"]).to_csv(filename, index=False) 


if __name__ == "__main__":
    start = time.time()
    print("Loading Location...")
    place_name = "Bulacan, Philippines"  
    locGraph = LocationGraph(place_name)

    print("Calculating shortest road distance...")
    results = calculate_distances_multithreaded(locations_list, locGraph)

    bad_triangles = check_triangle_inequality(results)
    if bad_triangles:
        print("Triangle inequality violations found:")
        for a,b,c,ab,bc,ac in bad_triangles:
            print(f"BAD: {a} to {b} + {b} to {c} ({ab:.2f} + {bc:.2f} = {ab + bc:.2f}) < {a} to {c} ({ac:.2f})")
    else:
        print("Triangle inequality holds for all triplets.")

    save_results_to_csv(results)
    print(f"Done! {(time.time() - start):.2f}s")
