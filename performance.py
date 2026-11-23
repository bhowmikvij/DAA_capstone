"""Benchmark major algorithms and generate CSV plus runtime chart."""
import csv
import random
import time
from pathlib import Path
from parcel_sorting import merge_sort_parcels
from knapsack import select_parcels
from graph_algorithms import build_graph, dijkstra
from route_optimizer import nearest_neighbor_route

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"

def timed_call(function, repeats=3):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        samples.append(time.perf_counter() - start)
    return sum(samples) / len(samples)

def make_parcels(count, seed=95):
    rng = random.Random(seed + count)
    return [{"parcel_id": f"P{i}", "customer_id": f"C{i}",
             "weight": rng.randint(1, 10), "deadline_hours": rng.uniform(1, 24),
             "priority": rng.randint(1, 5), "value": rng.randint(10, 100)}
            for i in range(count)]

def make_graph(count):
    # A connected chain plus deterministic shortcut edges.
    edges = [(f"N{i}", f"N{i+1}", 1 + (i % 7)) for i in range(count - 1)]
    for i in range(count - 2):
        edges.append((f"N{i}", f"N{i+2}", 3 + (i % 5)))
    return build_graph(edges)

def main():
    RESULTS.mkdir(exist_ok=True)
    rows = []
    for size in (20, 50, 100, 200):
        parcels = make_parcels(size)
        graph = make_graph(max(10, size))
        capacity = 100
        rows.append({"dataset_size": size, "algorithm": "Merge Sort",
                     "runtime_seconds": timed_call(lambda: merge_sort_parcels(parcels), 5)})
        rows.append({"dataset_size": size, "algorithm": "Built-in sorted",
                     "runtime_seconds": timed_call(lambda: sorted(parcels, key=lambda p: (-p["priority"], p["deadline_hours"], p["parcel_id"])), 5)})
        # Keep DP dimensions manageable and show how item count affects runtime.
        dp_items = parcels[:min(size, 120)]
        rows.append({"dataset_size": size, "algorithm": "0/1 Knapsack DP",
                     "runtime_seconds": timed_call(lambda: select_parcels(dp_items, capacity), 3)})
        rows.append({"dataset_size": size, "algorithm": "Dijkstra",
                     "runtime_seconds": timed_call(lambda: dijkstra(graph, "N0"), 3)})
        stops = [f"N{i}" for i in range(1, min(8, max(2, size // 10)) + 1)]
        rows.append({"dataset_size": size, "algorithm": "Nearest Neighbor",
                     "runtime_seconds": timed_call(lambda: nearest_neighbor_route(graph, "N0", stops), 3)})

    csv_path = RESULTS / "runtime_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["dataset_size", "algorithm", "runtime_seconds"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved runtime measurements: {csv_path}")

    try:
        import matplotlib.pyplot as plt
        chart_path = RESULTS / "runtime_chart.png"
        algorithms = sorted({row["algorithm"] for row in rows})
        sizes = sorted({row["dataset_size"] for row in rows})
        for algorithm in algorithms:
            values = [next(row["runtime_seconds"] for row in rows
                           if row["algorithm"] == algorithm and row["dataset_size"] == size)
                      for size in sizes]
            plt.plot(sizes, values, marker="o", label=algorithm)
        plt.xlabel("Input size (number of parcels / graph vertices)")
        plt.ylabel("Average runtime (seconds)")
        plt.title("Courier Planner - Algorithm Runtime Comparison")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=160)
        plt.close()
        print(f"Saved runtime chart: {chart_path}")
    except ImportError:
        print("Matplotlib is not installed. Run: python -m pip install matplotlib")

if __name__ == "__main__":
    main()
