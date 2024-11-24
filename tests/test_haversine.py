import unittest
import sys 
sys.path.append('/Users/eddie/Desktop/Iliad')
from iss_speed_calculation import haversine

class TestHaversine(unittest.TestCase):
    def test_valid_coordinates(self):
        lat1, lon1 = 40.7128, -74.0060  # New York
        lat2, lon2 = 34.0522, -118.2437  # Los Angeles
        expected_distance = 3936.0  # approximate distance in km
        self.assertAlmostEqual(haversine(lat1, lon1, lat2, lon2), expected_distance, delta=10)

    def test_identical_coordinates(self):
        lat, lon = 40.7128, -74.0060  # New York
        self.assertEqual(haversine(lat, lon, lat, lon), 0)

    def test_none_coordinates(self):
        self.assertIsNone(haversine(None, None, None, None))
        self.assertIsNone(haversine(40.7128, -74.0060, None, None))

if __name__ == "__main__":
    unittest.main()
