from quantplay.strategy.base import QuantplayAlgorithm
from quantplay.utils.constant import TickInterval
from quantplay.service import market
from quantplay.order_execution.mean_price import MeanPriceExecutionAlgo
import numpy as np


class Musk(QuantplayAlgorithm):
    def __init__(self):

        # Mandatory Attributes
        self.interval = TickInterval.minute
        self.entry_time = "09:29"
        self.exit_time = "15:15"
        self.strategy_trigger_times = [self.entry_time]
        self.exchange_to_trade_on = "NFO"
        self.option_nearest_expiry_offset = 0
        self.option_chain_depth = 0
        self.backtest_after_date = "2021-01-01"
        self.backtest_before_date = "2022-02-25"
        self.stream_symbols_by_security_type = {"EQ": ["NIFTY 50", "NIFTY BANK"]}
        self.columns_for_uuid = ["date", "symbol"]
        self.exact_number_of_orders_per_uuid = 2
        self.strategy_type = "intraday"
        self.strategy_tag = "musk"
        self.execution_algo = MeanPriceExecutionAlgo(7)

        # Optional Attribute
        self.data_required_for_days = 20

        super(Musk, self).__init__()

    def get_trades(self, market_data):

        equity_data = market_data[market_data.security_type == "EQ"]

        unique_equity_symbols = list(equity_data.symbol.unique())
        assert len(unique_equity_symbols) == 2
        assert set(unique_equity_symbols) == {"NIFTY 50", "NIFTY BANK"}

        trades = market.get_trades(equity_data, entry_time_regex=self.entry_time)

        trades = self.add_expiry(trades, security_type="OPT")
        trades = trades[trades.date.dt.year >= 2019]

        trades = trades[trades.strike_gap > 0]
        trades.loc[:, "atm_price"] = (
            round(trades.close / trades.strike_gap) * trades.strike_gap
        )
        trades.loc[:, "atm_price"] = trades.atm_price.astype(int)

        pe_trades = market.option_symbol(
            trades, price_column="atm_price", option_type="PE"
        )
        ce_trades = market.option_symbol(
            trades, price_column="atm_price", option_type="CE"
        )

        trades = pe_trades.append(ce_trades, sort=False).sort_values(["date"])

        trades.loc[:, "day_of_week"] = trades.date.dt.day_name()
        trades = trades[trades.day_of_week.isin(["Tuesday", "Wednesday", "Thursday"])]

        trades.loc[:, "transaction_type"] = "SELL"
        trades.loc[:, "stoploss"] = np.where(trades.symbol == "NIFTY 50", 0.5, 0.8)
        trades.loc[:, "quantity"] = np.where(trades.symbol == "NIFTY 50", 100, 50)

        trades = self.filter_uuids_not_matching_count(trades)

        return trades


if __name__ == "__main__":
    a, b = Musk().backtest()
    print(a)
