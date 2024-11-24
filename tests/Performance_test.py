import unittest
from unittest.mock import patch, MagicMock
import time
import sys
sys.path.append('/Users/eddie/Desktop/Iliad')  # Adjust path as needed
from iss_speed_calculation import track_iss_speed

class TestTrackIssSpeedPerformance(unittest.TestCase):
    @patch('iss_speed_calculation.get_iss_position')
    @patch('iss_speed_calculation.save_results_to_json')
    def test_performance(self, mock_save, mock_get):
        # Mocking ISS position responses
        mock_get.side_effect = [
            (40.7128, -74.0060, 1609459200),  # Initial position
            (40.7129, -74.0061, 1609459260),  # Slight movement
        ] * 100  # Repeat responses for multiple iterations
        
        mock_save.return_value = None
        
        # Measure performance
        start_time = time.time()
        results = track_iss_speed(max_runtime=10, poll_interval=0.1)
        elapsed_time = time.time() - start_time
        
        # Assertions
        self.assertGreater(len(results), 0, "Results should not be empty.")
        self.assertGreaterEqual(mock_get.call_count, 95, "Unexpected number of API calls (too few).")
        self.assertLessEqual(elapsed_time, 12, "Function took too long to execute.")
        self.assertTrue(all('iss_position' in res for res in results), "All results should contain ISS position data.")
        mock_save.assert_called()

if __name__ == "__main__":
    unittest.main()
