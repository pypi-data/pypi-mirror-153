import unittest

from quantplay.executor.strategy_executor import UserStrategiesExecutor


class QuantplayStrategyExecutorValidation(unittest.TestCase):
    def test_go_live(self):
        UserStrategiesExecutor("Zerodha", "quantplay/strategy", ["Musk"])


if __name__ == "__main__":
    unittest.main()
