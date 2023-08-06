from quantplay.strategy.base import QuantplayAlgorithm
from quantplay.utils.constant import TickInterval
from quantplay.service import market
from quantplay.order_execution.mean_price import MeanPriceExecutionAlgo
import pandas as pd
from datetime import datetime, time, timedelta
import numpy as np
from quantplay.utils.constant import Constants


class Ladder(QuantplayAlgorithm):
    def __init__(self):
        # Mandatory Attributes
        self.interval = TickInterval.minute
        self.entry_time = "^(09|10):.*$"
        self.exit_time = "15:15"
        self.strategy_trigger_times = [self.entry_time]
        self.exchange_to_trade_on = "NFO"
        self.stream_symbols_by_security_type = {"EQ": ["NIFTY 50"]}
        self.option_nearest_expiry_offset = 0
        self.strategy_type = "intraday"
        self.strategy_tag = "ladder"
        self.execution_algo = MeanPriceExecutionAlgo(15)

        # Optional Attribute
        self.data_required_for_days = 20

        super(Ladder, self).__init__()

    def get_trades(self, market_data):
        # load data
        equity_data = market_data[market_data.security_type == "EQ"]
        option_data = market_data[market_data.security_type == "OPT"]
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

        trades.loc[:, "transaction_type"] = "SELL"
        trades.loc[:, "stoploss"] = np.where(trades.symbol == "NIFTY 50", 0.5, 0.8)
        trades.loc[:, "quantity"] = np.where(trades.symbol == "NIFTY 50", 100, 50)

        # trades = pd.merge(
        #     option_data[["date", "symbol", "close"]].rename(
        #         columns={"symbol": "tradingsymbol", "close": "premium"}
        #     ),
        #     trades,
        #     how="left",
        #     left_on=["tradingsymbol", "date"],
        #     right_on=["tradingsymbol", "date"],
        # )

        option_data.loc[:, "date_only"] = pd.to_datetime(option_data.date.dt.date)

        trades = trades[trades.date.dt.time >= time(9, 29)]
        trades = (
            trades.sort_values(["date"], ascending=True)
            .groupby(["date_only", "tradingsymbol"])
            .first()
            .reset_index()
        )

        trades = trades.groupby("date_only").apply(
            self.create_ladder,
            options_data=option_data.rename(
                columns={"symbol": "tradingsymbol", "close": "premium"}
            ),
        )

        trades = trades[trades.new_trade == "Y"]

        return trades

    def create_ladder(self, grouped_df, options_data):
        records = grouped_df.to_dict("records")
        results = {"tradingsymbol": [], "new_trade": [], "quantity": []}

        start = datetime.now().replace(hour=9, minute=29)
        end = datetime.now().replace(hour=10, minute=59)
        records_idx = 0
        active_pe_symbol, active_ce_symbol = None, None
        active_ce_symbol_data, active_pe_symbol_data = None, None
        pe_sl, ce_sl = 0, 0

        while start <= end and records_idx < len(records):
            record = records[records_idx]
            date, tradingsymbol, stoploss, quantity, date_only = (
                record["date"],
                record["tradingsymbol"],
                record["stoploss"],
                record["quantity"],
                record["date_only"],
            )

            while start.time() < date.time():
                start += timedelta(minutes=1)

            if tradingsymbol.endswith("CE"):
                if not active_ce_symbol:
                    active_ce_symbol = tradingsymbol
                    results["tradingsymbol"].append(tradingsymbol)
                    results["new_trade"].append("Y")
                    results["quantity"].append(quantity)
                    active_ce_symbol_data = options_data[
                        (options_data.tradingsymbol == tradingsymbol)
                        & (options_data.date_only == date_only)
                        & (
                            options_data.date.dt.time.astype(str).str.match(
                                self.entry_time
                            )
                        )
                    ]
                    premium = active_ce_symbol_data[
                        (active_ce_symbol_data.date.dt.hour == start.hour)
                        & (active_ce_symbol_data.date.dt.minute == start.minute)
                    ].to_dict("records")[0]["premium"]
                    ce_sl = Constants.round_to_tick(premium * (1 + stoploss))
                else:
                    active_ce_symbol_premium = active_ce_symbol_data[
                        (active_ce_symbol_data.date.dt.hour == start.hour)
                        & (active_ce_symbol_data.date.dt.minute == start.minute)
                    ].to_dict("records")[0]["premium"]
                    if ce_sl < active_ce_symbol_premium:
                        results["tradingsymbol"].append(tradingsymbol)
                        results["new_trade"].append("N")
                        results["quantity"].append(quantity)
                    else:
                        active_ce_symbol = tradingsymbol
                        results["tradingsymbol"].append(tradingsymbol)
                        results["new_trade"].append("Y")
                        results["quantity"].append(quantity)
                        active_ce_symbol_data = options_data[
                            (options_data.tradingsymbol == tradingsymbol)
                            & (options_data.date_only == date_only)
                            & (
                                options_data.date.dt.time.astype(str).str.match(
                                    self.entry_time
                                )
                            )
                        ]
                        premium = active_ce_symbol_data[
                            (active_ce_symbol_data.date.dt.hour == start.hour)
                            & (active_ce_symbol_data.date.dt.minute == start.minute)
                        ].to_dict("records")[0]["premium"]
                        ce_sl = Constants.round_to_tick(premium * (1 + stoploss))

            elif tradingsymbol.endswith("PE"):
                if not active_pe_symbol:
                    active_pe_symbol = tradingsymbol
                    results["tradingsymbol"].append(tradingsymbol)
                    results["new_trade"].append("Y")
                    results["quantity"].append(quantity)
                    active_pe_symbol_data = options_data[
                        (options_data.tradingsymbol == tradingsymbol)
                        & (options_data.date_only == date_only)
                        & (
                            options_data.date.dt.time.astype(str).str.match(
                                self.entry_time
                            )
                        )
                    ]
                    premium = active_pe_symbol_data[
                        (active_pe_symbol_data.date.dt.hour == start.hour)
                        & (active_pe_symbol_data.date.dt.minute == start.minute)
                    ].to_dict("records")[0]["premium"]
                    pe_sl = Constants.round_to_tick(premium * (1 + stoploss))
                else:
                    active_pe_symbol_premium = active_pe_symbol_data[
                        (active_pe_symbol_data.date.dt.hour == start.hour)
                        & (active_pe_symbol_data.date.dt.minute == start.minute)
                    ].to_dict("records")[0]["premium"]
                    if pe_sl < active_pe_symbol_premium:
                        results["tradingsymbol"].append(tradingsymbol)
                        results["new_trade"].append("N")
                        results["quantity"].append(quantity)
                    else:
                        active_pe_symbol = tradingsymbol
                        results["tradingsymbol"].append(tradingsymbol)
                        results["new_trade"].append("Y")
                        results["quantity"].append(quantity)
                        active_pe_symbol_data = options_data[
                            (options_data.tradingsymbol == tradingsymbol)
                            & (options_data.date_only == date_only)
                            & (
                                options_data.date.dt.time.astype(str).str.match(
                                    self.entry_time
                                )
                            )
                        ]
                        premium = active_pe_symbol_data[
                            (active_pe_symbol_data.date.dt.hour == start.hour)
                            & (active_pe_symbol_data.date.dt.minute == start.minute)
                        ].to_dict("records")[0]["premium"]
                        pe_sl = Constants.round_to_tick(premium * (1 + stoploss))

            start += timedelta(minutes=1)
        grouped_df = pd.DataFrame(results)
        return grouped_df


if __name__ == "__main__":
    ladder = Ladder()
    ladder.validate()
    ladder.backtest(before="2022-02-25 00:00:00")
