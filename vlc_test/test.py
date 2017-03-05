import time
import unittest
import video

LINK = '/home/user/Video/Sample.avi'


class Basic(unittest.TestCase):
    def setUp(self):
        video.open_media(LINK)

    def tearDown(self):
        video.player.stop()

    def test_one(self):
        video.player.play()
        time.sleep(30)
        video.player.stop()
        assert False
