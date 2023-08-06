from quantplay.service import market, backtesting
import pandas as pd
import numpy as np

exit_time = "9:20"
entry_time = "15:15"
entry_hour, entry_minute = [int(a) for a in entry_time.split(":")]

nifty_minute_data = market.data(symbols=["NIFTY 50"], interval="minute")
trades = market.get_trades(nifty_minute_data, minute=entry_minute, hour=entry_hour)
trades = market.add_expiry(trades)

trades = trades[trades.strike_spread > 0]

trades.loc[:, "pe_price"] = (trades.close * 0.97 / trades.strike_spread).astype(
    int
) * trades.strike_spread.astype(int)
pe_trades = market.option_symbol(trades, price_column="pe_price", option_type="PE")
trades.loc[:, "ce_price"] = (trades.close * 1.03 / trades.strike_spread).astype(
    int
) * trades.strike_spread.astype(int)
ce_trades = market.option_symbol(trades, price_column="ce_price", option_type="CE")

trades = pe_trades.append(ce_trades, sort=False)

trades.loc[:, "stoploss"] = 0.25
trades.loc[:, "transaction_type"] = "SELL"
results, trades_res = backtesting.evaluate_performance(
    trades, entry_time=entry_time, exit_time=exit_time
)
trades_res[
    ["tradingsymbol", "entry_time", "entry_price", "exit_time", "close_price"]
].sort_values(["entry_time"]).head(10)
