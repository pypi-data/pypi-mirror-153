import unittest

from quantplay.strategy.musk import Musk


class QuantplayStrategyValidation(unittest.TestCase):
    def test_musk_execution(self):
        musk = Musk()
        musk.validate()
        result, trades = musk.backtest(
            before="2022-02-27 00:00:00", after="2022-01-01 00:00:00"
        )

        actual_trades = trades[trades.date_only == "2022-02-24"]
        actual_trades = actual_trades.to_dict("records")

        put_trades = [a for a in actual_trades if "PE" in a["tradingsymbol"]]
        call_trades = [a for a in actual_trades if "CE" in a["tradingsymbol"]]

        assert len(put_trades) == 2
        assert len(call_trades) == 2

        nifty_put_trade = [a for a in put_trades if a["symbol"] == "NIFTY 50"][0]
        nifty_call_trade = [a for a in call_trades if a["symbol"] == "NIFTY 50"][0]
        bank_nifty_put_trade = [a for a in put_trades if a["symbol"] == "NIFTY BANK"][0]
        bank_nifty_call_trade = [a for a in call_trades if a["symbol"] == "NIFTY BANK"][0]

        self.assertEqual(nifty_put_trade["tradingsymbol"], "NIFTY22FEB16650PE")
        self.assertEqual(nifty_put_trade["entry_price"], 101.3)
        self.assertEqual(nifty_put_trade["close_price"], 151.95)
        self.assertEqual(nifty_put_trade["quantity"], 100)

        self.assertEqual(nifty_call_trade["tradingsymbol"], "NIFTY22FEB16650CE")
        self.assertEqual(nifty_call_trade["entry_price"], 93.45)
        self.assertEqual(nifty_call_trade["close_price"], 0.20)
        self.assertEqual(nifty_call_trade["quantity"], 100)

        self.assertEqual(bank_nifty_put_trade["tradingsymbol"], "BANKNIFTY22FEB36400PE")
        self.assertEqual(bank_nifty_put_trade["entry_price"], 269.10)
        self.assertEqual(bank_nifty_put_trade["close_price"], 484.40)
        self.assertEqual(bank_nifty_put_trade["quantity"], 50)

        self.assertEqual(bank_nifty_call_trade["tradingsymbol"], "BANKNIFTY22FEB36400CE")
        self.assertEqual(bank_nifty_call_trade["entry_price"], 249.10)
        self.assertEqual(bank_nifty_call_trade["close_price"], 0.40)
        self.assertEqual(bank_nifty_call_trade["quantity"], 50)


if __name__ == "__main__":
    unittest.main()
