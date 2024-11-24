'''
This test handles scenatios where the network is unreachable, ensuring proper error handeling, and hanles rapid position changes to check if the system reacts as expected
'''

import unittest
from unittest.mock import patch
import sys
from io import StringIO
sys.path.append('/Users/eddie/Desktop/Iliad')
from iss_speed_calculation import get_iss_position
import requests


class TestEdgeCases(unittest.TestCase):

    @patch('requests.get')
    def test_no_network_connection(self, mock_get):
        print("\nRunning test: test_no_network_connection")
        # Simulate a network failure (API unreachable)
        mock_get.side_effect = requests.exceptions.RequestException("Network is unreachable")
        
        # Redirect stdout to suppress the print output
        with patch('sys.stdout', new=StringIO()):
            lat, lon, timestamp1 = get_iss_position()
        
        print("Simulated network error. Expected latitude and longitude to be None.")
        # Validate that the program correctly handles the network error
        self.assertIsNone(lat, "Latitude should be None if there's a network issue.")
        self.assertIsNone(lon, "Longitude should be None if there's a network issue.")
        print("Test passed: Network error was handled correctly, and None values were returned.")

    @patch('requests.get')
    def test_rapid_position_changes(self, mock_get):
        print("\nRunning test: test_rapid_position_changes")
        # Simulate rapid changes in position
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'message': 'success',
            'iss_position': {
                'latitude': '48.4406',
                'longitude': '-87.2757'
            },
            'timestamp': 1234567890

        }
        
        # Redirect stdout to suppress the print output
        with patch('sys.stdout', new=StringIO()):
            lat1, lon1 ,timestamp1 = get_iss_position()
        print(f"Initial position: Latitude = {lat1}, Longitude = {lon1}, TimeStamp={timestamp1}")

        # Simulate rapid change in position (quick update)
        mock_get.return_value.json.return_value = {
            'message': 'success',
            'iss_position': {
                'latitude': '48.4410',
                'longitude': '-87.2750'
            },
            'timestamp': 1234567891
        }
        
        # Get updated position
        with patch('sys.stdout', new=StringIO()):
            lat2, lon2, timestamp2 = get_iss_position()
        print(f"Updated position: Latitude = {lat2}, Longitude = {lon2}")
        
        # Ensure the positions have changed
        self.assertNotEqual(lat1, lat2, "Position should change rapidly.")
        self.assertNotEqual(lon1, lon2, "Position should change rapidly.")
        self.assertNotEqual(timestamp1, timestamp2, "Timestamp should change for rapid updates.")
        print("Test passed: Rapid position change detected correctly.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
