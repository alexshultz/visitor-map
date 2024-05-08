import unittest
from unittest.mock import patch
from src.services.geolocation import GeoLocator


class TestGeoLocator(unittest.TestCase):
    def setUp(self):
        self.geo = GeoLocator()

    @patch('src.services.geolocation.requests.get')
    def test_get_coordinates_successful(self, mock_get):
        # Setup mock
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'lat': '40.7128', 'lon': '-74.0060'}]

        # Action
        latitude, longitude = self.geo.get_coordinates('New York', 'NY', 'USA')

        # Assert
        self.assertEqual(latitude, '40.7128')
        self.assertEqual(longitude, '-74.0060')

    @patch('src.services.geolocation.requests.get')
    def test_get_coordinates_failure(self, mock_get):
        # Setup mock
        mock_get.return_value.status_code = 404

        # Action
        result = self.geo.get_coordinates('Nowhere', 'Nowhere', 'Nowhere')

        # Assert
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

    @patch('src.services.geolocation.requests.get')
    def test_state_only_query(self, mock_get):
        # Setup mock response for vague query
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"lat": "38.27312", "lon": "-98.5821872", "display_name": "Kansas, United States"},
            {"lat": "11.0", "lon": "31.0", "display_name": "South Kordofan, Sudan"}  # Incorrect result
        ]

        # Test vague input
        latitude, longitude = self.geo.get_coordinates('', 'KS', '')
        self.assertEqual((latitude, longitude), ('38.27312', '-98.5821872'))  # Assuming we handle picking the correct one

    @patch('src.services.geolocation.requests.get')
    def test_state_and_country_query(self, mock_get):
        # Setup mock for specific query
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"lat": "38.27312", "lon": "-98.5821872", "display_name": "Kansas, United States"}
        ]

        # Test specific input
        latitude, longitude = self.geo.get_coordinates('', 'KS', 'US')
        self.assertEqual((latitude, longitude), ('38.27312', '-98.5821872'))


if __name__ == '__main__':
    unittest.main()
