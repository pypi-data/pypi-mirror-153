# Import libraries
from quantplay.service import market, backtesting
import pandas as pd
import numpy as np
import talib

# load data
nifty_minute_data = market.data(symbols=["NIFTY 50"], interval="minute")
trades = market.get_trades(nifty_minute_data, minute=25, hour=15)
trades.loc[:, "cc_return"] = trades.close / trades.close.shift(1) - 1
trades.loc[:, "sma_20"] = talib.SMA(
    trades.close.replace([np.inf, -np.inf, np.nan], 0), timeperiod=20
)

trades = backtesting.add_time(trades, "15:25", "9:23")
trades.loc[:, "exit_time"] = trades.exit_time.shift(-1)
trades = trades[trades["exit_time"].notna()]

trades = market.add_expiry(trades)
trades = trades[trades.entry_time.dt.year >= 2021]
trades = trades[trades.close > trades.sma_20]
trades = trades[trades.date_only != trades.expiry_date]

trades = trades[trades.strike_spread > 0]
trades.loc[:, "otm_price"] = (trades.close * 0.985 / trades.strike_spread).astype(
    int
) * trades.strike_spread.astype(int)
pe_trades = market.option_symbol(trades, price_column="otm_price", option_type="PE")

trades.loc[:, "otm_price"] = (trades.close * 1.015 / trades.strike_spread).astype(
    int
) * trades.strike_spread.astype(int)
ce_trades = market.option_symbol(trades, price_column="otm_price", option_type="CE")

trades = pe_trades.append(ce_trades, sort=False).sort_values(["date"])

trades.loc[:, "tag"] = "straddle"
trades.loc[:, "transaction_type"] = "SELL"
trades.loc[:, "quantity"] = 300

results, trades_res = backtesting.evaluate_performance(trades, strategy_type="overnight")

trades_res.loc[:, "point"] = trades_res.entry_price - trades_res.close_price
trades_res = trades_res[trades_res.entry_price > 8]
trades_res.point.mean()
trades_res["day_of_week"] = trades_res["entry_time"].dt.day_name()
trades_res.groupby(["day_of_week"]).point.mean()
trades_res[trades_res.day_of_week == "Wednesday"][
    [
        "tradingsymbol",
        "entry_time",
        "entry_price",
        "exit_time",
        "close_price",
        "point",
    ]
].sort_values(["point"]).head(20)
