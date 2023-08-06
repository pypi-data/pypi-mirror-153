from quantplay.service import market, backtesting
import pandas as pd
import numpy as np

exit_time = "15:15"
entry_time = "9:29"
entry_hour, entry_minute = [int(a) for a in entry_time.split(":")]

nifty_minute_data = market.data(symbols=["NIFTY 50"], interval="minute")
nifty_minute_data = nifty_minute_data[nifty_minute_data.date.dt.year == 2022]
trades = market.get_trades(nifty_minute_data, minute=entry_minute, hour=entry_hour)
trades = market.add_expiry(trades)


trades = trades[trades.strike_spread > 0]
trades.loc[:, "atm_price"] = (trades.close / trades.strike_spread).astype(
    int
) * trades.strike_spread.astype(int)
pe_trades = market.option_symbol(trades, price_column="atm_price", option_type="PE")
ce_trades = market.option_symbol(trades, price_column="atm_price", option_type="CE")

trades = pe_trades.append(ce_trades, sort=False)

trades.loc[:, "stoploss"] = 0.25
trades.loc[:, "transaction_type"] = "SELL"
results, trades_res = backtesting.evaluate_performance(
    trades, entry_time=entry_time, exit_time=exit_time
)


trades_res[
    ["tradingsymbol", "entry_time", "entry_price", "exit_time", "close_price"]
].sort_values(["entry_time"]).tail(10)
