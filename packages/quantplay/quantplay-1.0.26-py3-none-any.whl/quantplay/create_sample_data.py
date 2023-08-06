from quantplay.service import market

symbols = market.symbols("NSE_INDICES") + market.symbols("NSE_ALL_STOCKS") + ["INDIA VIX"]
interval = "5minute"
market_data = market.data(
    symbols_by_security_type={
        "EQ": market.symbols("NSE_INDICES")
        + market.symbols("NSE_ALL_STOCKS")
        + ["INDIA VIX"]
    },
    interval=interval,
)
market_data = market_data[market_data.date >= "2021-12-01 00:00:00"]
market_data = market_data[market_data.date < "2022-01-01 00:00:00"]

symbols = market_data.symbol.unique()

for symbol in symbols:
    print("Saving data for {}".format(symbol))
    symbol_data = market_data[market_data.symbol == symbol][
        ["symbol", "date", "open", "high", "low", "close"]
    ]
    symbol_data.to_csv(
        "~/Documents/QuantplaySampleData/NSE_EQ/{}/{}.csv".format(interval, symbol),
        index=False,
    )
