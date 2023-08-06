from quantplay.strategy.base import QuantplayAlgorithm
from quantplay.utils.constant import TickInterval
from quantplay.service import market
from quantplay.order_execution.mean_price import MeanPriceExecutionAlgo
import numpy as np
import pandas as pd


class BUCS(QuantplayAlgorithm):
    def __init__(self):

        # Mandatory Attributes
        self.interval = TickInterval.minute
        self.entry_time = "15:27"
        self.exit_time = "09:16"
        self.strategy_trigger_times = [self.entry_time]
        self.exchange_to_trade_on = "NFO"
        self.option_nearest_expiry_offset = 1
        self.stream_symbols_by_security_type = {"EQ": ["NIFTY 50", "NIFTY BANK"]}
        self.columns_for_uuid = ["date", "symbol"]
        self.exact_number_of_orders_per_uuid = 2
        self.holding_days = 1
        self.strategy_type = "overnight"
        self.strategy_tag = "bucs"
        self.execution_algo = MeanPriceExecutionAlgo(7)

        # Optional Attribute
        self.data_required_for_days = 20
        self.option_chain_depth = 10
        self.backtest_before_date = "2022-02-25 00:00:00"
        self.backtest_after_date = "2020-01-01 00:00:00"

        super(BUCS, self).__init__()

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

        option_data = market_data[market_data.security_type == "OPT"]
        option_data.loc[:, "date_only"] = pd.to_datetime(option_data.date.dt.date)
        option_data.loc[:, "day_of_week"] = option_data.date.dt.day_name()

        # option_data = option_data.sort_values(["symbol", "date"])
        # option_data.loc[:, "vwap"] = option_data.close
        # option_data.loc[:, "vwap"] = option_data["vwap"] * option_data["volume"]
        # option_data.loc[:, "vwap"] = (
        #     option_data.groupby(["symbol", "date_only"])["vwap"].cumsum()
        #     / option_data.groupby(["symbol", "date_only"])["volume"].cumsum()
        # )

        option_data = market.get_trades(option_data, entry_time_regex=self.entry_time)

        # option_data = option_data[option_data.close > option_data.vwap]

        market.add_columns_in_option_data(
            option_data, columns=["equity_symbol", "option_type"]
        )

        option_data = option_data[option_data.option_type == "CE"]

        option_data = pd.merge(
            option_data,
            trades[["date", "symbol", "atm_price", "strike_gap", "expiry_date"]].rename(
                columns={"symbol": "equity_symbol"}
            ),
            how="left",
            left_on=["date", "equity_symbol"],
            right_on=["date", "equity_symbol"],
        )

        option_data = option_data[~option_data.expiry_date.isna()]

        option_data = market.filter_contracts_matching_expiry_date(option_data)

        market.add_columns_in_option_data(option_data, columns=["strike_price"])

        option_data.loc[:, "days_since_expiry"] = (
            option_data.expiry_date - option_data.date_only
        ).dt.days

        days_expiry_to_otm_pct_offset = {
            7: 10,
            6: 10,
            5: 10,
            4: 8,
            3: 8,
            2: 6,
            1: 5,
        }

        atm_ce_trades = option_data[
            option_data.strike_price == (option_data.atm_price + option_data.strike_gap)
        ]
        atm_ce_trades.loc[:, "transaction_type"] = "BUY"

        otm_ce_trades = option_data[
            option_data.strike_price
            == (
                option_data.atm_price
                + option_data.days_since_expiry.map(days_expiry_to_otm_pct_offset)
                * option_data.strike_gap
            )
        ]
        otm_ce_trades.loc[:, "transaction_type"] = "SELL"

        deep_otm_ce_trades = option_data[
            option_data.strike_price
            == (
                option_data.atm_price
                + (option_data.days_since_expiry.map(days_expiry_to_otm_pct_offset) + 1)
                * option_data.strike_gap
            )
        ]
        deep_otm_ce_trades.loc[:, "transaction_type"] = "SELL"

        trades = pd.concat([atm_ce_trades, otm_ce_trades, deep_otm_ce_trades], axis=0)

        trades = trades.rename(
            columns={"equity_symbol": "symbol", "symbol": "tradingsymbol"}
        )

        # trades = trades[
        #     trades.day_of_week.isin(["Tuesday", "Wednesday", "Thursday", "Friday"])
        # ]

        trades.loc[:, "quantity"] = np.where(trades.symbol == "NIFTY 50", 100, 50)
        # trades.loc[:, "stoploss"] = np.where(trades.symbol == "NIFTY 50", 0.5, 0.8)

        trades = self.filter_uuids_not_matching_count(trades)

        return trades


if __name__ == "__main__":
    BUCS().backtest()
