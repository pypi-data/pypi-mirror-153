import unittest

from quantplay.strategy.base import QuantplayAlgorithm


class QuantplayAlgorithmValidation(unittest.TestCase):
    def test_max_len_strategy_tag(self):
        self.assertEqual(QuantplayAlgorithm.MAX_LEN_FOR_STRATEGY_TAG, 8)


if __name__ == "__main__":
    unittest.main()
