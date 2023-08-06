# Import libraries
from quantplay.service import market, backtesting
import pandas as pd
import numpy as np
import talib

# load data
nifty_minute_data = market.data(symbols=["NIFTY 50"], interval="minute")
trades = market.get_trades(nifty_minute_data, hour=9, minute=29)

trades = backtesting.add_time(trades, "9:29", "15:10")

trades = market.add_expiry(trades)
trades = trades[trades.entry_time.dt.year >= 2019]

trades = trades[trades.strike_spread > 0]
trades.loc[:, "atm_price"] = (trades.close / trades.strike_spread).astype(
    int
) * trades.strike_spread.astype(int)

pe_trades = market.option_symbol(trades, price_column="atm_price", option_type="PE")
ce_trades = market.option_symbol(trades, price_column="atm_price", option_type="CE")

trades = pe_trades.append(ce_trades, sort=False).sort_values(["date"])

trades.loc[:, "tag"] = "straddle"
trades.loc[:, "transaction_type"] = "SELL"
trades.loc[:, "stoploss"] = 0.3
trades.loc[:, "quantity"] = 300

results, trades_res = backtesting.evaluate_performance(trades, strategy_type="intraday")

trades_res.loc[:, "point"] = trades_res.entry_price - trades_res.close_price
trades_res.point.mean()
trades_res["day_of_week"] = trades_res["entry_time"].dt.day_name()
trades_res.groupby(["day_of_week"]).point.mean()
trades_res[
    [
        "tradingsymbol",
        "entry_time",
        "entry_price",
        "exit_time",
        "close_price",
        "point",
    ]
].sort_values(["point"]).tail(70)
