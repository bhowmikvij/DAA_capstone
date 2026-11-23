"""Integrated courier planning application."""
import csv
from pathlib import Path
from parcel_sorting import merge_sort_parcels
from knapsack import select_parcels
from graph_algorithms import build_graph, dijkstra, reconstruct_path
from route_optimizer import nearest_neighbor_route

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VEHICLE_CAPACITY_KG = 25
DEPOT = "DEPOT"

def load_parcels(path):
    with open(path, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    for parcel in rows:
        for field in ("weight", "priority", "value"):
            parcel[field] = int(parcel[field])
        parcel["deadline_hours"] = float(parcel["deadline_hours"])
    return rows

def load_edges(path):
    with open(path, newline="", encoding="utf-8") as file:
        return [(row["from"], row["to"], float(row["distance"]))
                for row in csv.DictReader(file)]

def run():
    parcels = load_parcels(DATA_DIR / "parcels.csv")
    edges = load_edges(DATA_DIR / "roads.csv")
    graph = build_graph(edges)

    print("=" * 66)
    print("        COURIER ROUTE & PACKING OPTIMIZER")
    print("        Bhowmik Vij | Roll No. 2501010195")
    print("=" * 66)

    ordered = merge_sort_parcels(parcels)
    print("\nPHASE 2A - PARCEL PRIORITIZATION (MERGE SORT)")
    for p in ordered:
        print(f'{p["parcel_id"]:>4} | customer={p["customer_id"]:<8} | '
              f'priority={p["priority"]} | deadline={p["deadline_hours"]:>4} h | '
              f'weight={p["weight"]:>2} kg | value={p["value"]}')

    selected, weight, value, dp = select_parcels(ordered, VEHICLE_CAPACITY_KG)
    print(f"\nPHASE 2B - 0/1 KNAPSACK (capacity={VEHICLE_CAPACITY_KG} kg)")
    for p in selected:
        print(f'  {p["parcel_id"]} -> {p["customer_id"]} '
              f'({p["weight"]} kg, value {p["value"]})')
    print(f"Selected {len(selected)} parcels | total weight={weight} kg | total value={value}")
    print(f"DP table dimensions: {len(dp)} rows x {len(dp[0])} capacity columns")

    customers = sorted({p["customer_id"] for p in selected})
    print("\nPHASE 3A - DIJKSTRA SHORTEST PATHS FROM DEPOT")
    for customer in customers:
        distances, previous = dijkstra(graph, DEPOT)
        path = reconstruct_path(previous, DEPOT, customer)
        print(f"  {DEPOT} -> {customer}: {' -> '.join(path) if path else 'unreachable'} "
              f"| distance={distances.get(customer, float('inf')):.1f} km")

    print("\nPHASE 3B - NEAREST-NEIGHBOR DELIVERY TOUR")
    route = nearest_neighbor_route(graph, DEPOT, customers)
    print("Visit order: " + " -> ".join(route["visit_order"]))
    print("Road path:   " + " -> ".join(route["expanded_path"]))
    print(f'Approximate round-trip distance: {route["distance"]:.1f} km')
    if route["unreachable"]:
        print("Unreachable customers: " + ", ".join(route["unreachable"]))
    print("\nPlanning complete. The TSP route is an approximation, not a guaranteed optimum.")

if __name__ == "__main__":
    run()
