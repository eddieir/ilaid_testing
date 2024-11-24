import unittest
from unittest.mock import patch
import sys 
sys.path.append('/Users/eddie/Desktop/Iliad')
from iss_speed_calculation import track_iss_speed, save_results_to_json
import os
import json


class TestTrackISSSpeed(unittest.TestCase):
    @patch('iss_speed_calculation.get_iss_position')
    @patch('iss_speed_calculation.save_results_to_json')
    def test_tracking_logic(self, mock_save, mock_get_position):
        # Mock ISS positions to simulate movement
        # Infinite generator for mock positions
        def mock_positions():
            while True:
                yield (48.8566, 2.3522)
                yield (48.8570, 2.3530)
        mock_get_position.side_effect = mock_positions()
        # Run the function for a very short runtime
        results = track_iss_speed(max_runtime=2, poll_interval=1)
        print(f"Results: {results}")
    
        self.assertGreater(len(results), 0, "Results should not be empty.")
        mock_save.assert_called()
    
    def test_json_file_creation(self):
        output_file = "test_iss_results.json"
        if os.path.exists(output_file):
            os.remove(output_file)
        track_iss_speed(max_runtime=2, poll_interval=1, output_file=output_file)
        self.assertTrue(os.path.exists(output_file), "Output JSON file was not created.")
        with open(output_file, 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, list, "Data in JSON file should be a list.")
        os.remove(output_file)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTrackISSSpeed)
    unittest.TextTestRunner(verbosity=2).run(suite)
