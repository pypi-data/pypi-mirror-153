from quantplay.strategy.base import QuantplayAlgorithm
from quantplay.utils.constant import TickInterval
from quantplay.service import market
from quantplay.order_execution.mean_price import MeanPriceExecutionAlgo
import numpy as np
import pandas as pd


class Boeing(QuantplayAlgorithm):
    def __init__(self):

        # Mandatory Attributes
        self.interval = TickInterval.minute
        self.entry_time = "09:25"
        self.exit_time = "15:25"
        self.strategy_trigger_times = [self.entry_time]
        self.exchange_to_trade_on = "NFO"
        self.option_nearest_expiry_offset = 0
        self.stream_symbols_by_security_type = {"EQ": ["NIFTY BANK", "INDIA VIX"]}
        self.columns_for_uuid = ["date", "symbol"]
        self.exact_number_of_orders_per_uuid = 1
        self.strategy_type = "intraday"
        self.strategy_tag = "boeing"
        self.execution_algo = MeanPriceExecutionAlgo(7)

        # Optional Attribute
        self.data_required_for_days = 20
        self.option_chain_depth = 8
        self.backtest_after_date = "2020-01-01"

        super(Boeing, self).__init__()

    def merge_vix_data(self, vix_data, data):
        vix_data.loc[:, "vix_sma"] = vix_data.close.rolling(300).mean()
        vix_data.loc[:, "vix_above_sma"] = np.where(
            vix_data.close > vix_data.vix_sma, 1, 0
        )

        data = pd.merge(
            data,
            vix_data[["vix_above_sma", "date"]],
            how="left",
            left_on=["date"],
            right_on=["date"],
        )

        return data

    def get_trades(self, market_data):
        market_data.loc[:, "date_only"] = pd.to_datetime(market_data.date.dt.date)
        market_data.loc[:, "day_of_week"] = market_data.date.dt.day_name()

        equity_data = market_data[market_data.security_type == "EQ"]
        vix_data = equity_data[equity_data.symbol == "INDIA VIX"]
        equity_data = equity_data[equity_data.symbol.isin(["NIFTY BANK"])]
        unique_equity_symbols = list(equity_data.symbol.unique())
        assert len(unique_equity_symbols) == 1
        assert set(unique_equity_symbols) == {"NIFTY BANK"}

        equity_data = self.merge_vix_data(vix_data, equity_data)

        trades = market.get_trades(equity_data, entry_time_regex=self.entry_time)

        trades = trades[trades.vix_above_sma == 1]

        trades = self.add_expiry(trades, security_type="OPT")
        trades = trades[trades.date.dt.year >= 2019]

        trades = trades[trades.strike_gap > 0]

        trades.loc[:, "itm_pe_price"] = (
            round((trades.close * 1.015) / trades.strike_gap) * trades.strike_gap
        )
        trades.loc[:, "itm_pe_price"] = trades.itm_pe_price.astype(int)

        pe_trades = market.option_symbol(
            trades, price_column="itm_pe_price", option_type="PE"
        )
        pe_trades.loc[:, "transaction_type"] = "SELL"

        trades = pe_trades

        trades.loc[:, "day_of_week"] = trades.date.dt.day_name()
        trades = trades[trades.day_of_week.isin(["Tuesday", "Wednesday"])]

        # trades.loc[:, "transaction_type"] = "SELL"
        trades.loc[:, "quantity"] = 100

        trades = self.filter_uuids_not_matching_count(trades)

        return trades


if __name__ == "__main__":
    a, b = Boeing().backtest()
    print(a)
