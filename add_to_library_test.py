import unittest
from add_to_library import is_album_match, is_soundtrack

class TestAddToLibraryMethods(unittest.TestCase):

    def test_isSoundtrack(self):
        self.assertTrue(is_soundtrack("various artists", "Road Trip"))
        self.assertTrue(is_soundtrack("Rent", "Original Broadway Cast Recording"))
        self.assertTrue(is_soundtrack("South Park", "Original Motion Picture Soundtrack"))
        self.assertFalse(is_soundtrack("Peter Gabriel", "So"))

    def test_isAlbumMatch(self):
        self.assertFalse(is_album_match("South Park", "Original Motion Picture Soundtrack", {'title': 'Zaytoun'}))
        self.assertFalse(is_album_match("Rent", "Original Broadway Cast Recording", {'title': 'Selections From Rent'}))


if __name__ == '__main__':
    unittest.main()