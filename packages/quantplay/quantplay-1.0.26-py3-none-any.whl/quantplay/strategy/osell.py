from quantplay.strategy.base import QuantplayAlgorithm
from quantplay.utils.constant import TickInterval
from quantplay.service import market
from quantplay.order_execution.mean_price import MeanPriceExecutionAlgo
import numpy as np
import pandas as pd


class OSell(QuantplayAlgorithm):
    def __init__(self):

        # Mandatory Attributes
        self.interval = TickInterval.minute
        self.entry_time = "^13:45"
        self.exit_time = "9:25"
        self.strategy_trigger_times = [self.entry_time]
        self.exchange_to_trade_on = "NFO"
        self.option_nearest_expiry_offset = 1
        self.stream_symbols_by_security_type = {
            "EQ": [
                "NIFTY 50",
                "NIFTY BANK",
            ]
        }
        self.columns_for_uuid = ["date", "symbol"]
        self.exact_number_of_orders_per_uuid = 1
        self.strategy_type = "overnight"
        self.strategy_tag = "osell"
        self.option_chain_depth = 15
        self.holding_days = 1
        self.backtest_after_date = "2021-01-01"
        self.backtest_before_date = "2022-01-15"
        self.execution_algo = MeanPriceExecutionAlgo(7)

        # Optional Attribute
        self.data_required_for_days = 20

        super(OSell, self).__init__()

    def validate_input(self, equity_data):
        unique_equity_symbols = list(equity_data.symbol.unique())
        assert len(unique_equity_symbols) == len(
            self.stream_symbols_by_security_type["EQ"]
        )
        assert set(unique_equity_symbols) == set(
            self.stream_symbols_by_security_type["EQ"]
        )

    def get_trades(self, market_data):
        market_data.loc[:, "date_only"] = pd.to_datetime(market_data.date.dt.date)
        market_data.loc[:, "sma"] = market_data.close.rolling(300).mean()

        equity_data = market_data[market_data.security_type == "EQ"]
        self.validate_input(equity_data)

        trades = market.get_trades(equity_data, entry_time_regex=self.entry_time)

        trades = trades[trades.close < trades.close.rolling(20).mean()]
        trades = trades[trades.close < trades.sma]

        trades = self.add_expiry(trades, security_type="OPT")
        trades = trades[trades.strike_gap > 0]
        trades.loc[:, "itm_price"] = (
            round(trades.close * 1.015 / trades.strike_gap) * trades.strike_gap
        )
        trades.loc[:, "itm_price"] = trades.itm_price.astype(int)

        pe_trades = market.option_symbol(
            trades, price_column="itm_price", option_type="PE"
        )

        trades = pe_trades

        trades.loc[:, "day_of_week"] = trades.date.dt.day_name()
        trades = trades[
            trades.day_of_week.isin(["Monday", "Tuesday", "Thursday", "Friday"])
        ]

        trades.loc[:, "transaction_type"] = "BUY"
        trades.loc[:, "quantity"] = np.where(
            trades.symbol == "NIFTY 50",
            100,
            50,
        )

        trades = self.filter_uuids_not_matching_count(trades)

        return trades


if __name__ == "__main__":
    a, b = OSell().backtest()
    print(a)
