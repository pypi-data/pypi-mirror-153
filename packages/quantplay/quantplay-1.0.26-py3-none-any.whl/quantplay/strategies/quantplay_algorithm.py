from quantplay.utils.constant import LoggerUtils
from quantplay.utils.constant import TickInterval
from quantplay.model.strategy.strategy_response import StrategyResponse
from quantplay.model.exchange.order import ExchangeOrder
from quantplay.utils.constant import Constants
import re
import copy
from quantplay.utils.constant import ExchangeName


class QuantplayAlgorithm:
    def __init__(self):
        self.trade_check_interval = TickInterval.minute
        self.columns_to_shift = []
        self.trades_fetched = {}
        pass

    def load_data(self):
        pass

    def prepare_data(self):
        raise NotImplementedError

    def filter_trades(self):
        raise NotImplementedError

    def get_trades(self):
        if self.mode == "prod" and self.exchange == ExchangeName.nfo:
            self.day_candle_data.loc[
                :, "actual_tradingsymbol"
            ] = self.day_candle_data.future_tradingsymbol.shift(1)
            self.day_candle_data.loc[:, "lot_size"] = self.day_candle_data.lot_size.shift(
                1
            )

        self.prepare_data()
        trades_df = self.filter_trades()

        trades_df.loc[:, "tag"] = self.tag
        trades_df.loc[:, "stoploss"] = self.stoploss
        trades_df.loc[:, "transaction_type"] = "BUY" if self.is_long else "SELL"
        trades_df.loc[:, "exposure"] = self.exposure
        trades_df.loc[:, "strategy_type"] = self.strategy_type
        trades_df.loc[:, "exchange"] = self.exchange

        return trades_df

    def set_attributes(self, vars):
        for var in vars:
            setattr(self, var, vars[var])
        log_file_prefix = "strategy-" + self.tag
        self.logger = LoggerUtils.setup_logger(log_file_prefix, log_file_prefix)

    def pre_trading_setup(self, columns_to_shift=None):
        pass

    def should_invoke(self, current_tick_date):
        tick_time_str = current_tick_date.strftime(Constants.hour_min_format)

        for candle_filter in self.candle_filters:
            x = re.search(candle_filter, tick_time_str)
            if x:
                return True
        return False

    def next(self, all_data, current_tick_date=None):
        response = StrategyResponse()
        if not self.should_invoke(current_tick_date):
            return response

        self.logger.info("Invoking {}".format(self.tag))

        key = "{}:{}".format(current_tick_date.hour, current_tick_date.minute)

        if key not in self.trades_fetched:
            self.day_candle_data = copy.deepcopy(all_data[TickInterval.day])
            self.candle_data = all_data[TickInterval.five_minute]
            self.current_tick_date = current_tick_date

            trades_df = self.get_trades()

            trades = trades_df.to_dict("records")

            self.all_trades = ExchangeOrder.get_exchange_orders(
                trades,
                product=self.product,
                oms_version=self.oms_version,
                exchange=self.exchange,
                is_long=self.is_long,
            )

            self.trades_fetched[key] = True

        todays_trades = [
            a for a in self.all_trades if str(a.order_timestamp) == str(current_tick_date)
        ]

        if len(todays_trades) > 0:
            for single_trade in todays_trades:
                stock = single_trade.tradingsymbol
                response.new_orders[stock] = single_trade

        return response
