import config
import helper
import unittest


class AudioTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_set_track_name(self):
        self.assertEqual(helper.set_track_name(1), "track_01.mp3")

    def test_calc_merge_track_num(self):
        self.assertEqual(helper.calc_merge_track_num(332, config.MAX_TRACKS), 3)


if __name__ == '__main__':
    unittest.main()
