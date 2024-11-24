import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('/Users/eddie/Desktop/Iliad')
from iss_speed_calculation import save_results_to_json

class TestSaveResultsToJson(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_save_success(self, mock_file):
        results = [{"timestamp": 1609459200, "iss_position": {"latitude": "40.7128", "longitude": "-74.0060"}}]
        
        # Call the function to save the results
        save_results_to_json(results, "test_results.json")
        
        # Assert the open function was called with the correct file and mode
        mock_file.assert_called_once_with("test_results.json", 'w')
        
        # Get the handle and check all the calls to the write method
        handle = mock_file()
        
        # Check that the write method was called with the expected formatted JSON in chunks
        expected_calls = [
            '[\n    {\n        "timestamp": 1609459200,\n        "iss_position": {\n            "latitude": "40.7128",\n            "longitude": "-74.0060"\n        }\n    }\n]'
        ]
        
        # Check that the mock file's write method was called with the expected formatted JSON
        handle.write.assert_has_calls([patch.call(call) for call in expected_calls])

    @patch("builtins.open", side_effect=PermissionError)
    def test_save_error(self, mock_file):
        results = [{"timestamp": 1609459200, "iss_position": {"latitude": "40.7128", "longitude": "-74.0060"}}]
        with self.assertRaises(PermissionError):
            save_results_to_json(results, "test_results.json")

if __name__ == "__main__":
    unittest.main()
