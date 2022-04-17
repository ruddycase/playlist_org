import audio
import unittest


class AudioTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_set_track_name(self):
        self.assertEqual(audio._set_track_name(1), "track_01.mp3")

    def test_calc_merge_track_num(self):
        self.assertEqual(audio._calc_merge_track_num(332), 3)


if __name__ == '__main__':
    unittest.main()
