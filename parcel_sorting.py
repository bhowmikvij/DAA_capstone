"""Merge Sort for parcel priority ordering."""
def parcel_key(parcel):
    # Higher priority first; earlier deadline first; stable ID tie-break.
    return (-int(parcel["priority"]), float(parcel["deadline_hours"]), str(parcel["parcel_id"]))

def merge_sort_parcels(parcels):
    """Return a new list ordered by priority and deadline using Merge Sort."""
    if len(parcels) <= 1:
        return list(parcels)
    middle = len(parcels) // 2
    left = merge_sort_parcels(parcels[:middle])
    right = merge_sort_parcels(parcels[middle:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if parcel_key(left[i]) <= parcel_key(right[j]):
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
