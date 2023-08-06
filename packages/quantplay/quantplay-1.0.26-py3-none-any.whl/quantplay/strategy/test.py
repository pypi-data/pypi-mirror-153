from quantplay.strategy.base import QuantplayAlgorithm
from quantplay.utils.constant import TickInterval
from quantplay.service import market
from quantplay.order_execution.mean_price import MeanPriceExecutionAlgo


class Test(QuantplayAlgorithm):
    def __init__(self):

        # Mandatory Attributes
        self.interval = TickInterval.minute
        self.entry_time = "13:32"
        self.exit_time = "15:15"
        self.strategy_trigger_times = [self.entry_time]
        self.exchange = "NSE"
        self.stream_symbols = {"NSE": ["IDEA"]}
        self.strategy_type = "intraday"
        self.strategy_tag = "test"
        self.execution_algo = MeanPriceExecutionAlgo(5)

        # Optional Attribute
        self.data_required_for_days = 20

    def get_trades(self, market_data):
        # load data
        trade_hour, trade_minute = [int(a) for a in self.entry_time.split(":")]
        trades = market.get_trades(market_data, hour=trade_hour, minute=trade_minute)

        trades.loc[:, "tradingsymbol"] = "IDEA"
        trades.loc[:, "transaction_type"] = "SELL"
        trades.loc[:, "stoploss"] = 0.03
        trades.loc[:, "quantity"] = 23

        return trades


if __name__ == "__main__":
    Musk().backtest()
