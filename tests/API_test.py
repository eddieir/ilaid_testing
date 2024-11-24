import unittest
from unittest.mock import patch
import sys 
sys.path.append('/Users/eddie/Desktop/Iliad')
import requests
from iss_speed_calculation import get_iss_position



class TestGetISSPosition(unittest.TestCase):
    @patch('iss_speed_calculation.requests.get')
    def test_valid_response(self, mock_get):
        """Test when the API response contains valid ISS position data."""
        mock_get.return_value.json.return_value = {
            "message": "success",
            "iss_position": {
                "latitude": "47.6062",
                "longitude": "-122.3321"
            },
            "timestamp": 1631568000
        }
        mock_get.return_value.status_code = 200
        result = get_iss_position()
        self.assertEqual(result, (47.6062, -122.3321, 1631568000), 
                         "Should return the correct latitude, longitude, and timestamp.")

    @patch('iss_speed_calculation.requests.get')
    def test_missing_iss_position(self, mock_get):
        """Test when the API response is missing the 'iss_position' key."""
        mock_get.return_value.json.return_value = {
            "message": "success",
            "timestamp": 1631568000
        }
        mock_get.return_value.status_code = 200
        result = get_iss_position()
        self.assertEqual(result, (None, None, 1631568000), 
                         "Should return (None, None, timestamp) for missing ISS position.")

    @patch('iss_speed_calculation.requests.get')
    def test_missing_lat_or_lon(self, mock_get):
        """Test when latitude or longitude is missing from the API response."""
        mock_get.return_value.json.return_value = {
            "message": "success",
            "iss_position": {
                "latitude": None,
                "longitude": "-122.3321"
            },
            "timestamp": 1631568000
        }
        mock_get.return_value.status_code = 200
        result = get_iss_position()
        self.assertEqual(result, (None, None, 1631568000), 
                         "Should return (None, None, timestamp) when latitude or longitude is missing.")

    @patch('iss_speed_calculation.requests.get')
    def test_api_timeout(self, mock_get):
        """Test when the API call times out."""
        mock_get.side_effect = requests.exceptions.Timeout
        result = get_iss_position()
        self.assertEqual(result, (None, None, None), 
                         "Should handle timeouts gracefully and return (None, None, None).")

    @patch('iss_speed_calculation.requests.get')
    def test_api_error_status(self, mock_get):
        """Test when the API returns a 500 Internal Server Error."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
        result = get_iss_position()
        self.assertEqual(result, (None, None, None), 
                         "Should return (None, None, None) on server error.")

    @patch('iss_speed_calculation.requests.get')
    def test_invalid_json(self, mock_get):
        """Test when the API response is not valid JSON."""
        # Mock the behavior where response.json() raises a ValueError for invalid JSON
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")
        result = get_iss_position()
        self.assertEqual(result, (None, None, None), 
                         "Should handle invalid JSON gracefully and return (None, None, None).")


if __name__ == '__main__':
    #Use a test loader to discover tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestGetISSPosition)
    
    # Run the tests with a verbose output
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
