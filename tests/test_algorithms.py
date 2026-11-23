import unittest
from parcel_sorting import merge_sort_parcels
from knapsack import select_parcels
from graph_algorithms import build_graph, dijkstra, reconstruct_path
from route_optimizer import nearest_neighbor_route

class TestCourierAlgorithms(unittest.TestCase):
    def test_merge_sort_priority_and_deadline(self):
        parcels = [
            {"parcel_id":"b","priority":2,"deadline_hours":1},
            {"parcel_id":"a","priority":3,"deadline_hours":4},
            {"parcel_id":"c","priority":3,"deadline_hours":2},
        ]
        self.assertEqual([p["parcel_id"] for p in merge_sort_parcels(parcels)], ["c","a","b"])

    def test_knapsack_capacity_and_optimum(self):
        parcels = [
            {"parcel_id":"A","weight":4,"value":40},
            {"parcel_id":"B","weight":3,"value":50},
            {"parcel_id":"C","weight":5,"value":60},
        ]
        selected, weight, value, dp = select_parcels(parcels, 8)
        self.assertEqual(weight, 8)
        self.assertEqual(value, 110)
        self.assertEqual({p["parcel_id"] for p in selected}, {"B","C"})
        self.assertEqual(dp[-1][-1], 110)

    def test_dijkstra_path(self):
        graph = build_graph([("S","A",2),("A","B",3),("S","B",9)])
        distances, previous = dijkstra(graph, "S")
        self.assertEqual(distances["B"], 5)
        self.assertEqual(reconstruct_path(previous, "S", "B"), ["S","A","B"])

    def test_nearest_neighbor_returns_to_depot(self):
        graph = build_graph([("D","A",2),("D","B",5),("A","B",2)])
        route = nearest_neighbor_route(graph, "D", ["A","B"])
        self.assertEqual(route["visit_order"][0], "D")
        self.assertEqual(route["visit_order"][-1], "D")
        self.assertAlmostEqual(route["distance"], 8)
        self.assertEqual(route["unreachable"], [])

    def test_negative_edges_rejected(self):
        with self.assertRaises(ValueError):
            build_graph([("A","B",-1)])

if __name__ == "__main__":
    unittest.main()
