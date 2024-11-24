import unittest
from unittest.mock import patch
import sys 
sys.path.append('/Users/eddie/Desktop/Iliad')
from iss_speed_calculation import track_iss_speed, get_iss_position

class TestTrackIssSpeed(unittest.TestCase):
    @patch('iss_speed_calculation.get_iss_position')
    @patch('iss_speed_calculation.save_results_to_json')
    def test_track_speed(self, mock_save, mock_get):
        # Mocking ISS position responses for multiple consecutive polls
        mock_get.side_effect = [
            (40.7128, -74.0060, 1609459200),  # Initial position
            (34.0522, -118.2437, 1609459260)  # New position after 1 minute
        ] * 5  # Repeat responses to cover max_runtime iterations
        
        mock_save.return_value = None  # Mock save method
        
        # Call the tracking function with a short runtime
        results = track_iss_speed(max_runtime=5, poll_interval=1)
        
        # Assertions to verify results
        self.assertGreater(len(results), 0)
        self.assertEqual(results[-1]['iss_position']['latitude'], "34.0522")
        self.assertEqual(results[-1]['iss_position']['longitude'], "-118.2437")

    @patch('iss_speed_calculation.get_iss_position')
    def test_invalid_position(self, mock_get):
        # Simulating invalid ISS positions
        mock_get.side_effect = [(None, None, None), (None, None, None)]
        
        # Call the tracking function
        results = track_iss_speed(max_runtime=5, poll_interval=1)
        
        # Assert that the result is an empty list
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()
