import unittest


class TestKML(unittest.TestCase):

    def test_LocationShouldBeList(self):

        location = None

        self.assertIsInstance(location, list)


if __name__ == '__main__':
    unittest.main()
