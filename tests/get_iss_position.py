import unittest
from unittest.mock import patch
import sys
sys.path.append('/Users/eddie/Desktop/Iliad')
from iss_speed_calculation import get_iss_position

class TestGetIssPosition(unittest.TestCase):
    @patch('requests.get')
    def test_api_success(self, mock_get):
        # Mocking a successful response with the updated JSON format
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "timestamp": 1732444144,
            "message": "success",
            "iss_position": {
                "latitude": "41.7387",
                "longitude": "65.2802"
            }
        }
        # Add a print statement for debugging
        print("Running test_api_success")
        lat, lon, timestamp = get_iss_position()
        print(f"Latitude: {lat}, Longitude: {lon}, Timestamp: {timestamp}")
        self.assertEqual(lat, 41.7387)
        self.assertEqual(lon, 65.2802)
        self.assertEqual(timestamp, 1732444144)

    @patch('requests.get')
    def test_api_failure(self, mock_get):
        # Simulating a failed request (e.g., network failure or 404 error)
        mock_get.return_value.status_code = 404
        lat, lon, timestamp = get_iss_position()
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        self.assertIsNone(timestamp)

    @patch('requests.get')
    def test_invalid_json(self, mock_get):
        # Simulating invalid JSON response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")
        lat, lon, timestamp = get_iss_position()
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        self.assertIsNone(timestamp)

if __name__ == "__main__":
    unittest.main()
