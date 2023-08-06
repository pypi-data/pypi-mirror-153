import glob
import pandas as pd
import numpy as np
import copy
import time
import threading
from collections import defaultdict
from datetime import datetime, timedelta
from quantplay.utils.constant import Constants, IntervalAttribute, TickInterval
from quantplay.model.exchange.tick import QuantplayTick
from quantplay.utils.exchange import Market
from quantplay.model.exchange.order import (
    QuantplayExchangeResponse,
    QuantplayExchangeResponseType,
    QuantplayTransactionStatus,
    QuantplayExchangeOrderStatus,
)
from quantplay.exception.exceptions import QuantplayOrderPlacementException
from queue import Queue, PriorityQueue
import traceback


class Broker:
    """Parent class for all brokerages."""

    def __init__(self, tick_intervals, live_trade, *args, **kwargs):
        """Initiates the broker object to be used for fetching either
        a) historical data, OR
        b) live trading

        :param: tick_intervals: list of tick_interval
        :param: live_trade: bool, set to True if the broker object is to
        be used for live trade
        """
        self.tick_intervals = tick_intervals
        self.live_trade = live_trade
        self.strategy_instruments = (
            []
        )  # Dataframe will be created for only these instruments. Subset of streaming_instruments
        self.streaming_instruments = (
            []
        )  # Data will be streamed for all of these instruments
        self.instrument_id_to_symbol_map = dict()
        self.instrument_id_to_exchange_map = dict()
        self.instrument_id_to_security_type_map = dict()
        self.exchange_symbol_to_instrument_id_map = defaultdict(dict)

        # Live Market Feed Members
        self.exchange_symbol_last_tick = defaultdict(dict)
        self.pre_market_volume = defaultdict(int)
        self.live_market_df_by_interval = {
            interval: pd.DataFrame() for interval in self.tick_intervals
        }
        self.ongoing_tick_interval_time = dict()
        self.ongoing_tick_updates = dict()
        self.last_updated_interval_tick = dict()
        self.processed_tick_interval_queue = Queue()

        # Order Execution Members
        self.strategy_child_orders = defaultdict(
            list
        )  # {strategy_tag: child_quantplay_order}
        self.last_processed_order_map = dict()  # {order_id: quantplay_order}
        self.in_progress_order_map = dict()  # {order_id: quantplay_order}
        self.next_modifications_queue = PriorityQueue()

        # map locks
        self.order_placement_lock = threading.Lock()

        for tick_interval in self.tick_intervals:
            self.ongoing_tick_updates[tick_interval] = {}
            self.ongoing_tick_interval_time[tick_interval] = None
            self.last_updated_interval_tick[tick_interval] = None

    def load_historical_market_feed(self, days):
        instrument_data_by_interval = defaultdict(list)

        for instrument_id in self.strategy_instruments:
            symbol = self.instrument_id_to_symbol_map[instrument_id]
            security_type = self.instrument_id_to_security_type_map[instrument_id]

            end_date = datetime.now()
            end_date = end_date.replace(second=0, microsecond=0)

            start_date = end_date - timedelta(days=days)
            start_date = start_date.replace(minute=0, hour=0)

            response = self.get_historical_data(
                instrument_id, start_date=start_date, end_date=end_date
            )
            for interval, data in response.items():
                if len(data) > 0:
                    data = self.add_today_candles(data, symbol)
                    data.loc[:, "security_type"] = security_type
                    instrument_data_by_interval[interval].append(data)
                else:
                    print(
                        "No historical data for symbol {} instrument_id {} interval {}".format(
                            symbol, instrument_id, interval
                        )
                    )

        for interval, df_list in instrument_data_by_interval.items():
            self.live_market_df_by_interval[interval] = pd.concat(df_list).reset_index(
                drop=True
            )

        self.reset_market_df_index()
        for interval in self.live_market_df_by_interval:
            self.live_market_df_by_interval["minute"].to_csv(
                f"/tmp/live_feed_{interval}.csv"
            )

    def add_today_candles(self, data, symbol):
        """Adds todays empty candles for the given interval to the data"""
        current_time = datetime.now()
        unique_times = data.date.dt.time.sort_values().unique()
        last_candle_time = data.iloc[-1].date.time()

        candles_to_add = []
        for candle_time in unique_times:
            if (data.iloc[-1].date.date() < datetime.now().date()) or (
                candle_time > last_candle_time
            ):
                candles_to_add.append(
                    {
                        "date": current_time.replace(
                            hour=candle_time.hour,
                            minute=candle_time.minute,
                            microsecond=0,
                            second=0,
                        ),
                        "symbol": symbol,
                    }
                )

        return data.append(candles_to_add, ignore_index=True)

    def populate_instruments(self, *args, **kwargs):
        """Fetches instruments for all exchanges from the broker
        and stores them in the member attributes.
        """
        pass

    def get_all_child_orders(self, *args, **kwargs):
        """Returns list of child orders by calling broker API"""
        pass

    def bootstrap_strategy_child_orders_map(self, strategies):
        """Bootstraps broker with child orders.

        :param: strategies: List[strategy objects]
        """
        print("Bootstrapping child orders map")
        tag_to_strategy_map = {s.strategy_tag: s for s in strategies}
        child_orders = self.get_all_child_orders()
        self.order_placement_lock.acquire()
        for order in child_orders:
            strategy = tag_to_strategy_map[order.tag]
            order.set_strategy_attributes(strategy)
            self.strategy_child_orders[order.tag].append(order)
            self.in_progress_order_map[order.order_id] = order
            print(f"Added Child Order {order}")
        self.order_placement_lock.release()
        print(f"Added {len(child_orders)} total child orders")

    def add_strategy_symbols(self, symbols, exchange):
        """Adds symbols for which either
        a) historical data needs to be fetched, or
        b) live market feed needs to be streamed

        It updates self.strategy_instruments with the instruments
        matching the given symbols and exchange
        """
        self.strategy_instruments += [
            self.exchange_symbol_to_instrument_id_map[exchange][symbol]
            for symbol in symbols
            if symbol in self.exchange_symbol_to_instrument_id_map[exchange]
        ]
        self.streaming_instruments = list(
            set(self.streaming_instruments + self.strategy_instruments)
        )

    def stream_new_symbols(self, instrument_ids):
        """Adds instrument_ids for which data needs to be streamed.

        Note that live_market_df_by_interval will not contain data for
        these instrument_ids. Only exchange_symbol_last_tick will have
        data for these instrument_ids
        """
        pass

    def connect(self):
        """To be used for final connect after assigning callbacks"""
        pass

    def is_valid_live_tick(self, tick):
        """Returns True if the tick is valid"""
        raise NotImplementedError

    def __upsert_ongoing_tick(
        self,
        interval,
        symbol,
        instrument_id,
        last_price,
        volume_till_now,
        initialize=False,
    ):
        if initialize:
            self.ongoing_tick_updates[interval][symbol] = {}
            self.ongoing_tick_updates[interval][symbol]["open"] = last_price
            self.ongoing_tick_updates[interval][symbol]["high"] = last_price
            self.ongoing_tick_updates[interval][symbol]["low"] = last_price
            self.ongoing_tick_updates[interval][symbol]["symbol"] = symbol
            self.ongoing_tick_updates[interval][symbol][
                "security_type"
            ] = self.instrument_id_to_security_type_map[instrument_id]

        self.ongoing_tick_updates[interval][symbol]["high"] = max(
            last_price, self.ongoing_tick_updates[interval][symbol]["high"]
        )
        self.ongoing_tick_updates[interval][symbol]["low"] = min(
            last_price, self.ongoing_tick_updates[interval][symbol]["low"]
        )
        self.ongoing_tick_updates[interval][symbol]["close"] = last_price
        self.ongoing_tick_updates[interval][symbol]["volume"] = volume_till_now
        self.ongoing_tick_updates[interval][symbol]["total_volume"] = volume_till_now

    def __add_interval_ticks_to_market_df(self, interval):

        date = np.datetime64(self.ongoing_tick_interval_time[interval])

        for symbol in self.ongoing_tick_updates[interval]:
            interval_tick = self.ongoing_tick_updates[interval][symbol]
            interval_tick["date"] = date
            for column_name in interval_tick:
                self.live_market_df_by_interval[interval].at[
                    (symbol, date), column_name
                ] = interval_tick[column_name]

        print(
            f"Added Tick {self.ongoing_tick_interval_time[interval]} for interval {interval} to market_df"
        )
        self.last_updated_interval_tick[interval] = self.ongoing_tick_interval_time[
            interval
        ]
        self.processed_tick_interval_queue.put(
            (interval, self.ongoing_tick_interval_time[interval])
        )

    def last_updated_interval_tick(self, interval):
        return self.last_updated_interval_tick[interval]

    def reset_market_df_index(self):

        for interval in self.tick_intervals:
            self.live_market_df_by_interval[interval].loc[
                :, "date_index"
            ] = self.live_market_df_by_interval[interval].date
            self.live_market_df_by_interval[interval].loc[
                :, "symbol_index"
            ] = self.live_market_df_by_interval[interval].symbol
            self.live_market_df_by_interval[interval] = self.live_market_df_by_interval[
                interval
            ].set_index(["symbol_index", "date_index"])
            self.live_market_df_by_interval[interval] = self.live_market_df_by_interval[
                interval
            ].sort_values(["symbol", "date"])

    def market_feed(self, ticks):
        """Stores live ticks for the instruments added in a dataframe.
        In addition, it also persists the live data on the disk

        :param: ticks: List[QuantplayTicks]
        """

        for interval in self.tick_intervals:

            mod_value = Constants.interval_attributes[interval][
                IntervalAttribute.mod_value
            ]

            for tick in ticks:
                if not self.is_valid_live_tick(tick):
                    continue

                orders_to_modify = self.get_orders_to_modify()
                if orders_to_modify:
                    for quantplay_order in orders_to_modify:
                        self.place_or_modify_order(quantplay_order, is_new_order=False)

                last_trade_time = tick.last_trade_time
                symbol = tick.symbol
                exchange = tick.exchange
                exchange_start_time = Market.TIMINGS[exchange]["start"]

                self.exchange_symbol_last_tick[exchange][symbol] = tick

                if tick.instrument_id not in self.strategy_instruments:
                    continue

                if interval == TickInterval.day:
                    tick_interval_time = last_trade_time.replace(
                        hour=exchange_start_time[0],
                        minute=exchange_start_time[1],
                        second=0,
                    )
                else:
                    minutes_since_market_start = (
                        last_trade_time.hour - exchange_start_time[0]
                    ) * 60 + (last_trade_time.minute - exchange_start_time[1])
                    tick_number = int(minutes_since_market_start / mod_value)
                    tick_interval_time = last_trade_time.replace(
                        hour=exchange_start_time[0],
                        minute=exchange_start_time[1],
                        second=0,
                    ) + timedelta(minutes=tick_number * mod_value)

                volume_till_now = tick.volume_traded - self.pre_market_volume[symbol]
                last_price = tick.last_price

                if self.ongoing_tick_interval_time[interval] is None:
                    self.ongoing_tick_interval_time[interval] = tick_interval_time

                if (symbol in self.ongoing_tick_updates[interval]) and (
                    self.ongoing_tick_interval_time[interval] == tick_interval_time
                ):
                    self.__upsert_ongoing_tick(
                        interval,
                        symbol,
                        tick.instrument_id,
                        last_price,
                        volume_till_now,
                        initialize=False,
                    )
                else:
                    if tick_interval_time > self.ongoing_tick_interval_time[interval]:
                        self.__add_interval_ticks_to_market_df(interval)

                        self.ongoing_tick_updates[interval] = {}
                        self.__upsert_ongoing_tick(
                            interval,
                            symbol,
                            tick.instrument_id,
                            last_price,
                            volume_till_now,
                            initialize=True,
                        )
                        self.ongoing_tick_interval_time[interval] = tick_interval_time

                    if symbol not in self.ongoing_tick_updates[interval]:
                        print(
                            "Found new tick for {} last_trade_time {} tick_interval_time {}".format(
                                symbol, last_trade_time, tick_interval_time
                            )
                        )
                        self.__upsert_ongoing_tick(
                            interval,
                            symbol,
                            tick.instrument_id,
                            last_price,
                            volume_till_now,
                            initialize=True,
                        )

    def get_orders_to_modify(self):
        """Checks self.next_modifications_queue for any pending orders
        and returns list of orders to be modified
        """
        orders_to_modify = []
        current_time = datetime.now()
        total_qsize = self.next_modifications_queue.qsize()
        in_progress_orders = []
        elements_processed = 0

        while elements_processed < total_qsize:
            modification_time, order_id = self.next_modifications_queue.get()
            if modification_time > current_time:
                self.next_modifications_queue.put((modification_time, order_id))
                break
            elif order_id in self.in_progress_order_map:
                in_progress_orders.append((modification_time, order_id))
            elif order_id in self.last_processed_order_map:
                orders_to_modify.append(self.last_processed_order_map[order_id])
            else:
                print(
                    f"not modifying order with order_id {order_id} as it is already confirmed"
                )

            elements_processed += 1

        for mod_time, order_id in in_progress_orders:
            self.next_modifications_queue.put((mod_time, order_id))

        return orders_to_modify

    def place_new_order(self, quantplay_order):
        """Translates quantplay order to broker order and calls the broker API
        for placing new orders. To be implemented in broker subclasses.

        Returns order_id, quantplay_order.
        """
        raise NotImplementedError

    def modify_exiting_order(self, quantplay_order):
        """Translates quantplay order to broker order and calls the broker API
        for modifying order. To be implemented in broker subclasses.

        Returns order_id, quantplay_order.
        """
        raise NotImplementedError

    def close_child_orders(self, tag=None):
        if not tag:
            print(f"Tag must be provided for closing child orders")
            return

        if tag not in self.strategy_child_orders:
            print(f"Strategy {tag} does not have any child orders")
            return

        child_orders = self.strategy_child_orders[tag]
        for order in child_orders:
            order.modify_child_order_for_closing()
            try:
                self.place_or_modify_order(order, is_new_order=False)
            except QuantplayOrderPlacementException as e:
                print(
                    f"[CHILD_ORDER_MODIFICATION_FOR_CLOSING_FAILED] Failed to modify order {order} got {e}"
                )
                traceback.print_exc()

    def place_or_modify_order(self, quantplay_order, is_new_order=True):
        """Places the new order or modifies an existing order and executes it using the
        given execution algorithm.

        It stores the given order and execution algorithm against the orderId.
        """

        exchange, tradingsymbol, execution_algo = (
            quantplay_order.exchange,
            quantplay_order.tradingsymbol,
            quantplay_order.execution_algo,
        )
        instrument_id = self.exchange_symbol_to_instrument_id_map[exchange][tradingsymbol]

        if instrument_id not in self.streaming_instruments:
            self.stream_new_symbols([instrument_id])

            while tradingsymbol not in self.exchange_symbol_last_tick[exchange]:
                print(
                    "Delaying order placement by 10ms as tick has not arrived for {}:{}".format(
                        exchange, tradingsymbol
                    )
                )
                time.sleep(0.1)

        self.order_placement_lock.acquire()
        try:
            if is_new_order:
                execution_algo.modify_order(
                    self.exchange_symbol_last_tick[exchange][tradingsymbol],
                    quantplay_order,
                    is_new_order=True,
                )

                order_id, quantplay_order = self.place_new_order(quantplay_order)
                print(f"[NEW_ORDER_REQUEST] order_id {order_id} order {quantplay_order}")

                if quantplay_order.is_child_order == False:
                    child_order = quantplay_order.get_child_order()
                    print(f"Placing child order {child_order}")
                    child_order_id, child_order = self.place_new_order(child_order)
                    print(
                        f"[CHILD_ORDER_PLACED] child_order_id {child_order_id} child_order {child_order}"
                    )
                    self.in_progress_order_map[child_order_id] = child_order
                    # TODO: Map order_id to child_order_id
            else:
                execution_algo.modify_order(
                    self.exchange_symbol_last_tick[exchange][tradingsymbol],
                    quantplay_order,
                    is_new_order=False,
                )
                order_id = quantplay_order.order_id
                quantplay_order = self.modify_existing_order(quantplay_order)
                print(
                    f"[MODIFY_ORDER_REQUEST] order_id {order_id} order {quantplay_order}"
                )
        except Exception as e:
            self.order_placement_lock.release()
            raise QuantplayOrderPlacementException(
                "Failed to place or modify order"
            ) from e

        self.in_progress_order_map[order_id] = quantplay_order
        self.order_placement_lock.release()

        seconds_since_modification = execution_algo.get_next_modification_time(
            self.exchange_symbol_last_tick[exchange][tradingsymbol],
            quantplay_order,
        )
        next_modification_time = quantplay_order.order_placement_time + timedelta(
            seconds=seconds_since_modification
        )
        self.next_modifications_queue.put((next_modification_time, order_id))

    def on_order_response(self, response: QuantplayExchangeResponse):
        """Processes the order response"""
        order_id = response.order_id
        message = response.message
        response_type = response.response_type
        quantity = response.quantity
        avg_price = response.average_price

        if response_type in [
            QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
            QuantplayExchangeResponseType.MOD_ORDER_CONFIRM,
            QuantplayExchangeResponseType.NEW_ORDER_REJECT,
            QuantplayExchangeResponseType.MOD_ORDER_REJECT,
        ]:

            in_progress_order = self.in_progress_order_map[order_id]
            del self.in_progress_order_map[order_id]

            if response_type in [
                QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
                QuantplayExchangeResponseType.MOD_ORDER_CONFIRM,
            ]:
                in_progress_order.transaction_status = (
                    QuantplayTransactionStatus.PROCESSED
                )
                in_progress_order.order_status = QuantplayExchangeOrderStatus.OPEN
                self.last_processed_order_map[order_id] = in_progress_order

            elif response_type == QuantplayExchangeResponseType.NEW_ORDER_REJECT:
                print(f"[NEW_ORDER_REJECT] response {response}")

            elif response_type == QuantplayExchangeResponseType.MOD_ORDER_REJECT:
                print(f"[MOD_ORDER_REJECT] response {response}")

        elif response_type == QuantplayExchangeResponseType.TRADE_CONFIRM:
            processed_order = self.last_processed_order_map[order_id]

            processed_order.filled_quantity += response.quantity
            if processed_order.quantity == processed_order.filled_quantity:
                processed_order.order_status = QuantplayExchangeOrderStatus.COMPLETE
                self.remove_order_from_order_maps(
                    order_id=processed_order.order_id, tag=processed_order.tag
                )

        elif response_type in [
            QuantplayExchangeResponseType.OMS_REJECT,
            QuantplayExchangeResponseType.RMS_REJECT,
        ]:
            pass
        elif response_type == QuantplayExchangeResponseType.CANCEL_ORDER_CONFIRM:
            print(f"[CANCEL_ORDER_CONFIRM] response {response}")
            self.remove_order_from_order_maps(order_id=order_id)
        elif response_type == QuantplayExchangeResponseType.TRIGGER_CONFIRM:
            in_progress_order = self.in_progress_order_map[order_id]
            self.strategy_child_orders[in_progress_order.tag].append(in_progress_order)
        else:
            print(f"[UNKNOWN_EXCHANGE_RESPONSE] {response}")

    def remove_order_from_order_maps(self, order_id, tag=None):

        if order_id in self.last_processed_order_map:
            del self.last_processed_order_map[order_id]

        if order_id in self.in_progress_order_map:
            print(
                f"[UNEXPECTED_IN_PROGRESS_ORDER_FOUND] order_id {order_id} is complete. Deleting its unexpected presence in in_progress_order_map"
            )
            del self.in_progress_order_map[order_id]

        if tag:
            print(
                f"Removing child order for tag {tag} with order_id {order_id} from strategy_child_orders map"
            )
            strategy_child_orders = self.strategy_child_orders[tag]
            strategy_child_orders_updated = [
                s_child_order
                for s_child_order in strategy_child_orders
                if s_child_order.order_id != order_id
            ]
            self.strategy_child_orders[tag] = strategy_child_orders_updated

    def get_processed_quantplay_order_by_id(self, order_id):
        """Returns the quantplay order which has been confirmed
        by the exchange for the order_id.

        Returns None if the order does not exist in memory.
        """
        self.order_placement_lock.acquire()
        order = None
        if order_id in self.last_processed_order_map:
            order = self.last_processed_order_map[order_id]
        self.order_placement_lock.release()
        return order

    def get_in_progress_quantplay_order_by_id(self, order_id):
        """Returns the quantplay order which has been requested
        to be put on the exchange for the order_id.

        Returns None if the order does not exist in memory.
        """
        self.order_placement_lock.acquire()
        order = None
        if order_id in self.in_progress_order_map:
            order = self.in_progress_order_map[order_id]
        self.order_placement_lock.release()
        return order

    def market_df(self, tick_interval):
        """Returns the market dataframe containing the live data
        for the provided interval
        """
        if tick_interval not in self.tick_intervals:
            raise Exception(
                f"Tick interval {tick_interval} has not been subscribed. Subscribed intervals: {self.tick_intervals}"
            )

        return copy.deepcopy(self.live_market_df_by_interval[tick_interval])

    def get_historical_data(self, instrument, start_date, end_date):
        """Fetches the historical data by calling the broker API.

        To Be Implemented in the actual broker's child class.
        """
        pass

    def store_historical_data(
        self, start_date, end_date, instruments=[], dataset_path="/NSE_EQ/"
    ):
        """Stores the historical data for the given instruments and given tick_intervals
        from start_date to end_date.from

        If the instruments argument is empty, data is stored for all the added instruments.
        """
        instruments_ids = instruments
        if not instruments_ids:
            instruments_ids = self.instruments

        if not instruments_ids:
            raise Exception(
                "Neither the instrument ids were given as argument nor they were added by calling add_instruments"
            )

        for instrument in instruments_ids:
            already_fetched_symbols = self.get_already_stored_symbols(
                dataset_path, interval
            )

            data_by_interval = self.get_historical_data(instrument, start_date, end_date)

    def get_already_stored_symbols(self, dataset_path, tick_interval):
        """Returns list of symbols which are already present at the dataset_path for
        the given tick_interval.
        """
        path = "{}{}/".format(dataset_path, tick_interval)

        symbols = [
            file.replace(path, "").replace(".csv", "")
            for file in glob.glob("{}*".format(path))
            if "csv" in file
        ]

        return symbol

    def store_data():
        main_instruments = self.get_instruments()
        end_date = datetime.now()

        if dataset_path == DatasetPath.NSE_EQ:
            main_instruments = self.get_equity_instruments(main_instruments)
        if dataset_path == DatasetPath.NSE_OPT:
            # fetching data of last 3 months only
            start_date = end_date - timedelta(days=100)
            main_instruments = self.filter_instruments(
                exchange="NFO", segment="NFO-OPT", name="NIFTY"
            )
        if dataset_path == DatasetPath.NSE_FUT:
            start_date = end_date - timedelta(days=100)
            main_instruments = self.filter_instruments(exchange="NFO", segment="NFO-FUT")

        for interval in intervals:
            already_fetched_symbols = self.get_already_stored_symbols(
                dataset_path, interval
            )

            with alive_bar(len(main_instruments), force_tty=True) as bar:
                for instrument in main_instruments:
                    fetch_from = start_date
                    symbol = instrument["tradingsymbol"]
                    symbol_data = []

                    try:
                        print("Fetching data of {} name [{}]".format(symbol, instrument))

                        if symbol in already_fetched_symbols:
                            try:
                                symbol_data = DataUtils.get_data(
                                    path=dataset_path,
                                    interval=interval,
                                    stocks=[symbol],
                                )
                                fetch_from = symbol_data.date.max().to_pydatetime()
                                print(
                                    "Data already stored for {}".format(
                                        instrument["tradingsymbol"]
                                    )
                                )
                            except Exception as e:
                                fetch_from = start_date
                                symbol_data = []
                        else:
                            print(
                                "{} not found on the disk".format(
                                    instrument["tradingsymbol"]
                                )
                            )

                        data = self.get_historical_data(
                            instrument, interval, fetch_from, end_date
                        )
                        data = pd.DataFrame(data)
                        if len(data) > 0:
                            data.loc[:, "date"] = data["date"].dt.tz_localize(None)
                            data.loc[:, "date"] = pd.to_datetime(data.loc[:, "date"])
                            data.loc[:, "symbol"] = instrument["tradingsymbol"]

                            if len(symbol_data) > 0:
                                data = FileUtils.merge_data(data, symbol_data)

                            FileUtils.save_file(
                                data,
                                instrument["tradingsymbol"],
                                interval,
                                dataset_path,
                            )
                    except Exception as e:
                        print("[FAILED_TO_FETCH_DATA] [{}] {}".format(symbol, e))
                    bar()
