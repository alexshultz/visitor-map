import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.services.kml_manager import KMLManager

class TestKMLManager(unittest.TestCase):

    def setUp(self):
        self.kml_manager = KMLManager(directory="/fake/directory")

    @patch('os.makedirs')
    @patch('os.remove')
    @patch('shutil.copy2')
    @patch('glob.glob')
    @patch('builtins.open', new_callable=mock_open, create=True)
    def test_update_static_data(self, mock_open, mock_glob, mock_copy, mock_remove, mock_makedirs):
        # Setup mocks to simulate file existence and operations
        mock_glob.return_value = ["/fake/directory/data_001.kml", "/fake/directory/data_002.kml"]
        mock_open().read.return_value = "<Placemark></Placemark>"

        # Call the function under test
        self.kml_manager.update_static_data()

        # Check if backups were made correctly
        expected_backup_calls = [
            call("/fake/directory/data_001.kml", "/fake/directory/backups/data_001.kml"),
            call("/fake/directory/data_002.kml", "/fake/directory/backups/data_002.kml")
        ]
        mock_copy.assert_has_calls(expected_backup_calls, any_order=True)

        # Verify that the static file was appended to
        mock_open.assert_called_with("/fake/directory/static_data.kml", 'a')
        handle = mock_open()
        handle.write.assert_called_with("<Placemark></Placemark><Placemark></Placemark>")

        # Ensure directory creation was attempted
        mock_makedirs.assert_called_with("/fake/directory/backups", exist_ok=True)

        # Ensure the cleanup of processed files
        mock_remove.assert_has_calls([
            call("/fake/directory/data_001.kml"),
            call("/fake/directory/data_002.kml")
        ], any_order=True)

if __name__ == '__main__':
    unittest.main()
