# DAA Capstone Report
## Courier Route and Packing Optimizer

**Student:** Bhowmik Vij  
**Roll Number:** 2501010195  
**Course:** Design and Analysis of Algorithms  
**Project type:** Python prototype

---

## Abstract
The Courier Route and Packing Optimizer demonstrates how multiple algorithmic techniques can be combined in a delivery-planning workflow. It sorts parcels by urgency, chooses a high-value feasible load under a vehicle capacity, computes shortest paths through a weighted road network, and estimates a delivery tour using the Nearest-Neighbor TSP heuristic. A separate benchmark script measures the runtime of the major components.

## Phase 1 — Courier problem design and planning

### Problem definition
A courier depot receives a list of parcels. Each parcel has a parcel ID, customer ID, weight, delivery deadline, priority and simulated value. The vehicle has a fixed weight capacity. Customers and the depot are vertices in a weighted road graph; road distances are edge weights.

### Data model
| Field | Meaning |
|---|---|
| parcel_id | Unique parcel identifier |
| customer_id | Delivery location identifier |
| weight | Parcel weight in kg (integer) |
| deadline_hours | Deadline measured from planning time |
| priority | Integer urgency score; larger means higher priority |
| value | Simulated benefit used by the knapsack objective |

The road CSV stores from, to and distance. The graph is undirected and uses positive edge weights. The depot is named DEPOT.

### Integrated workflow
1. Read parcel and road CSV files.
2. Apply Merge Sort using priority descending, then deadline ascending.
3. Apply 0/1 Knapsack DP to choose a maximum-value subset within vehicle capacity.
4. Run Dijkstra from the depot to show individual shortest paths to selected customers.
5. Apply Nearest Neighbor to visit selected customers and return to the depot, using shortest road distances between stops.
6. Benchmark the algorithms and save a CSV plus chart.

### Design flow
```text
Parcels CSV + Roads CSV
          |
          v
  Merge Sort (priority/deadline)
          |
          v
  0/1 Knapsack DP (capacity)
          |
          v
  Selected customer locations
          |
          +------> Dijkstra (individual shortest paths)
          |
          v
  Nearest-Neighbor TSP approximation
          |
          v
  Delivery order + route distance
          |
          v
  Performance benchmark and report
```

## Phase 2 — Package prioritization and box filling

### Merge Sort
The comparison key is (-priority, deadline_hours, parcel_id). Thus a larger priority score appears first; equal-priority parcels with earlier deadlines appear first. Merge Sort divides the list into halves, sorts both halves recursively and merges them.

**Time complexity:** O(n log n)  
**Auxiliary space:** O(n)

### 0/1 Knapsack Dynamic Programming
Each parcel can either be selected once or not selected. Let DP[i][w] be the maximum value achievable using the first i parcels with capacity w.

```text
DP[0][w] = 0
DP[i][w] = DP[i-1][w]                         if weight[i] > w
DP[i][w] = max(DP[i-1][w],
               value[i] + DP[i-1][w-weight[i]]) otherwise
```

The implementation stores the complete DP table and backtracks through it to recover the selected parcel IDs.

**Time complexity:** O(nW)  
**Space complexity:** O(nW)  
Here, n is parcel count and W is integer vehicle capacity.

The sample vehicle capacity is 25 kg. The program prints the selected parcels, total weight, total value and DP table dimensions.

## Phase 3 — Route maker and graph processing

### Graph representation
An adjacency dictionary stores each vertex and its neighboring vertices with edge distances. This representation supports efficient neighbor iteration.

### Dijkstra's algorithm
Dijkstra starts the source distance at zero and all other distances at infinity. It repeatedly chooses the unvisited vertex with the smallest tentative distance, then relaxes its outgoing edges. A predecessor dictionary reconstructs the actual road path.

The implementation uses a linear search to find the next minimum-distance vertex.

**Time complexity:** O(V² + E) with this simple selection method.  
**Space complexity:** O(V + E) for the graph and O(V) auxiliary distance/predecessor data.

### Nearest-Neighbor TSP approximation
Start at the depot. Repeatedly travel to the nearest unvisited selected customer, where distance between stops is the shortest-path distance from Dijkstra. Once all reachable selected customers are visited, return to the depot if a path exists.

The heuristic is simple and fast but does not guarantee the globally shortest Hamiltonian tour. Unreachable destinations are listed separately.

**Tour construction complexity:** O(k²) after shortest-path distances are available in the conceptual complete metric graph. This implementation runs Dijkstra for each chosen leg, so its practical cost also includes those shortest-path computations.

## Phase 4 — Performance testing and optimization

Run:
```bash
python performance.py
```

The script creates results/runtime_results.csv and results/runtime_chart.png (requires Matplotlib).

It measures Merge Sort, Python built-in sorting, 0/1 Knapsack DP, Dijkstra and Nearest Neighbor over increasing generated input sizes. Each measurement is averaged over repeated runs. The benchmark is synthetic and measures local execution time; results vary with CPU, operating system and Python version.

### Interpretation and possible improvements
- Built-in sorting may be faster because it is implemented in optimized native code; Merge Sort is included to demonstrate the algorithm taught in DAA.
- Knapsack runtime grows with both item count and capacity. Large capacities can make the DP table expensive.
- A min-heap can reduce Dijkstra's cost on sparse graphs to O((V+E) log V).
- Caching all-pairs shortest-path distances for selected stops avoids rerunning Dijkstra for each tour leg.
- A 2-opt local-search pass or another TSP heuristic may improve the Nearest-Neighbor tour.
- Real delivery planning would also need time windows, parcel dimensions, traffic, service times and vehicle constraints.

**Evidence to insert after local execution:** Add the generated runtime chart and screenshots of actual program output to the screenshots/ folder. Do not invent or manually estimate measured runtimes.

## Phase 5 — Final report and demonstration

### Demonstration sequence
1. Show the input CSV files and explain the parcel and graph fields.
2. Run python main.py; explain the Merge Sort ordering and knapsack selection.
3. Explain one Dijkstra path and the final approximate route.
4. Run the unit tests with python -m unittest discover -s tests -v.
5. Run python performance.py; open the CSV and runtime chart.
6. Discuss complexity, assumptions, limitations and possible improvements.

### Validation
The automated tests cover:
- Merge Sort priority/deadline ordering.
- Knapsack capacity and optimal value for a small known case.
- Dijkstra shortest path and path reconstruction.
- Nearest-Neighbor route closure and distance on a small graph.
- Rejection of negative edge weights.

### Limitations
- Deadlines are used for ordering, not as hard time-window constraints.
- Parcel value is a sample objective, not a real revenue calculation.
- The knapsack uses integer weights and capacity.
- The road network is synthetic and static.
- Nearest Neighbor is approximate and can return a suboptimal route.
- This is a prototype, not a production dispatch system.

### Student reflection
Before submission, the student should run the application independently, inspect the outputs, add genuine screenshots, and be prepared to explain the algorithm steps and complexity in their own words.
