# softassert.py usage example
import unittest
import softassert

class TestSoftAssert(unittest.TestCase):
    def test_sa(self):
        with softassert.SoftAssert() as sa:
            # self.assertEqual(1, 2, "one_two") becomes:
            sa(self.assertEqual, 1, 2, "one_two")
            # same as above:
            sa(self.assertEqual, 2, 3, "two_three")
            # self.assertGreater(5, 6, "greater56") becomes:
            sa(self.assertGreater, 5, 6, "greater56")
