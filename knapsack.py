"""0/1 Knapsack solved with bottom-up Dynamic Programming."""
def select_parcels(parcels, capacity):
    """Maximize total parcel value without exceeding integer weight capacity.

    Returns (selected_parcels, total_weight, total_value, dp_table).
    dp_table[i][w] is the best value using the first i parcels and capacity w.
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    if any(int(p["weight"]) < 0 for p in parcels):
        raise ValueError("Parcel weights cannot be negative")
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight = int(parcels[i - 1]["weight"])
        value = int(parcels[i - 1]["value"])
        for limit in range(capacity + 1):
            dp[i][limit] = dp[i - 1][limit]
            if weight <= limit:
                candidate = dp[i - 1][limit - weight] + value
                if candidate > dp[i][limit]:
                    dp[i][limit] = candidate
    selected = []
    remaining = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            remaining -= int(parcel["weight"])
    selected.reverse()
    total_weight = sum(int(p["weight"]) for p in selected)
    total_value = sum(int(p["value"]) for p in selected)
    return selected, total_weight, total_value, dp
