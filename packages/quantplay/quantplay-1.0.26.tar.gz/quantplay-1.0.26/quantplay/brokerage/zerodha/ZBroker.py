from quantplay.brokerage.generics.broker import Broker
import pickle
import codecs
import time
from collections import defaultdict
from datetime import timedelta, datetime
from retrying import retry
import pandas as pd
from typing import List, Tuple
from quantplay.utils.data_utils import DataUtils
from quantplay.config.qplay_config import QplayConfig
from quantplay.model.exchange.instrument import QuantplayInstrument
from quantplay.model.exchange.tick import QuantplayTick
from quantplay.model.exchange.order import (
    QuantplayExchangeOrder,
    QuantplayExchangeResponseType,
    QuantplayExchangeResponse,
)
from quantplay.service import market
from alive_progress import alive_bar
from kiteconnect import KiteTicker


class DatasetPath:
    NSE_EQ = "/NSE_EQ/"
    NSE_OPT = "/NSE_OPT/"
    NSE_FUT = "/NSE_FUT/"


class ZerodhaServiceConstants:
    zerodha_token = "ZERODHA_TOKEN"
    # TODO rename it to kite_object
    kite_object = "kite_object"
    default_api_type = "default"


class ZBroker(Broker):
    """Zerodha Broker"""

    def __init__(self, tick_intervals, live_trade):
        kite_str = QplayConfig.get_value(ZerodhaServiceConstants.kite_object)
        self.kite = pickle.loads(codecs.decode(kite_str.encode(), "base64"))
        self.kws = KiteTicker(self.kite.api_key, self.kite.access_token)
        try:
            self.kite.orders()
        except Exception as e:
            raise Exception(
                "Looks like token has expired. Please regenerate it through 'quantplay broker generate-token'"
            ) from e

        super(ZBroker, self).__init__(tick_intervals, live_trade)

        self.populate_instruments()

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def populate_instruments(self):
        """Calls zerodha's populate_instruments API and populates instrument mappings."""
        instruments = self.kite.instruments()
        instruments = list(
            map(
                lambda z_instrument: QuantplayInstrument.from_zerodha_instrument(
                    z_instrument
                ),
                instruments,
            )
        )
        for instrument in instruments:
            exchange, symbol, instrument_id = (
                instrument.exchange,
                instrument.symbol,
                instrument.instrument_id,
            )
            self.instrument_id_to_symbol_map[instrument_id] = symbol
            self.instrument_id_to_exchange_map[instrument_id] = exchange
            self.instrument_id_to_security_type_map[
                instrument_id
            ] = instrument.security_type()
            self.exchange_symbol_to_instrument_id_map[exchange][symbol] = instrument_id

    def add_strategy_symbols(self, symbols, exchange):
        super(ZBroker, self).add_strategy_symbols(symbols, exchange)
        if self.live_trade:
            print("assigning callbacks")
            self.initiate_live_trade_callbacks()

    def get_all_child_orders(self):
        orders_data = self.kite.orders()
        trigger_orders = [
            QuantplayExchangeOrder.from_zerodha_order(data, is_child_order=True)
            for data in orders_data
            if data["status"] == "TRIGGER PENDING" and "tag" in data
        ]
        return trigger_orders

    def place_new_order(self, quantplay_order):
        data = quantplay_order.to_zerodha_order()
        print("Placing new order through Zerodha {}".format(data))

        try:
            order_id = self.kite.place_order(
                variety=data["variety"],
                tradingsymbol=data["tradingsymbol"],
                exchange=data["exchange"],
                transaction_type=data["transaction_type"],
                quantity=int(abs(data["quantity"])),
                order_type=data["order_type"],
                disclosed_quantity=data["disclosed_quantity"],
                price=data["price"],
                trigger_price=data["trigger_price"],
                product=data["product"],
                stoploss=data["stoploss"],
                tag=data["tag"],
                squareoff=data["squareoff"],
            )
        except Exception as e:
            exception_message = "Order placement failed for [{}] with error [{}]".format(
                quantplay_order, str(e)
            )
            raise Exception(exception_message) from e

        quantplay_order.order_placement_time = datetime.now()
        quantplay_order.order_id = order_id
        return order_id, quantplay_order

    def modify_existing_order(self, quantplay_order):
        data = quantplay_order.to_zerodha_order()
        order_id = quantplay_order.order_id

        try:
            response = self.kite.modify_order(
                order_id=order_id,
                variety=data["variety"],
                price=data["price"],
                trigger_price=data["trigger_price"],
                disclosed_quantity=data["disclosed_quantity"],
                order_type=data["order_type"],
            )

            print(f"Successfully modified order {response}")
        except Exception as e:
            exception_message = (
                "OrderModificationFailed for {} failed with exception {}".format(
                    order_id, e
                )
            )
            raise Exception(exception_message) from e

        quantplay_order.order_placement_time = datetime.now()
        return quantplay_order

    def stream_new_symbols(self, instrument_ids):
        self.streaming_instruments = list(
            set(self.streaming_instruments + instrument_ids)
        )
        self.kws.subscribe(self.streaming_instruments)
        self.kws.set_mode(self.kws.MODE_FULL, self.streaming_instruments)

    def connect(self):
        self.kws.connect()

    def initiate_live_trade_callbacks(self):
        self.kws.on_connect = self.on_connect
        self.kws.on_ticks = self.on_ticks
        self.kws.on_order_update = self.on_order_update

    def on_connect(self, kws, response):
        """Callback on successfull connect"""
        kws.subscribe(self.streaming_instruments)
        kws.set_mode(kws.MODE_FULL, self.streaming_instruments)

    def on_ticks(self, kws, ticks):
        """Callback on live ticks"""
        quantplay_ticks = list(
            map(
                lambda t: QuantplayTick.from_zerodha_tick(
                    t,
                    self.instrument_id_to_symbol_map,
                    self.instrument_id_to_exchange_map,
                ),
                ticks,
            )
        )
        super(ZBroker, self).market_feed(quantplay_ticks)

    def on_order_update(self, kws, data):
        """Callback on order update"""
        order_id, status, status_message = (
            data["order_id"],
            data["status"],
            data["status_message"],
        )
        quantity, filled_quantity, pending_quantity = (
            data["quantity"],
            data["filled_quantity"],
            data["pending_quantity"],
        )
        average_price = data["average_price"]

        log_message = (
            f"order_id {order_id} status {status} status_message {status_message}"
        )

        print(f"order_update {log_message} full_data {data}")

        last_processed_order = super(ZBroker, self).get_processed_quantplay_order_by_id(
            order_id
        )
        in_progress_order = super(ZBroker, self).get_in_progress_quantplay_order_by_id(
            order_id
        )

        responses: List[Tuple[QuantplayExchangeResponseType, int, float]] = []
        quantity = 0
        if last_processed_order:
            quantity = filled_quantity - last_processed_order.filled_quantity

        if status == "COMPLETE":
            if not last_processed_order:
                if not in_progress_order:
                    print(
                        f"[DROPPING_COMPLETE_RESPONSE] order_id {order_id} not in memory"
                    )
                    return
                else:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
                            0,
                            0.0,
                        )
                    )
            responses.append(
                (
                    QuantplayExchangeResponseType.TRADE_CONFIRM,
                    quantity,
                    average_price,
                )
            )
        elif status == "UPDATE":
            if not last_processed_order:
                if not in_progress_order:
                    print(f"[DROPPING_UPDATE_RESPONSE] order_id {order_id} not in memory")
                    return
                elif not status_message:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
                            0,
                            0.0,
                        )
                    )
                    responses.append(
                        (
                            QuantplayExchangeResponseType.TRADE_CONFIRM,
                            quantity,
                            0.0,
                        )
                    )
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.NEW_ORDER_REJECT, 0, 0.0)
                    )
            else:
                if not in_progress_order:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.TRADE_CONFIRM,
                            quantity,
                            0.0,
                        )
                    )
                elif not status_message:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.MOD_ORDER_CONFIRM,
                            0,
                            0.0,
                        )
                    )
                    responses.append(
                        (
                            QuantplayExchangeResponseType.TRADE_CONFIRM,
                            quantity,
                            0.0,
                        )
                    )
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.MOD_ORDER_REJECT, 0, 0.0)
                    )
        elif status == "OPEN":
            if not last_processed_order:
                if not in_progress_order:
                    print(f"[DROPPING_OPEN_RESPONSE] order_id {order_id} not in memory")
                    return
                else:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
                            0,
                            0.0,
                        )
                    )
                    responses.append(
                        (
                            QuantplayExchangeResponseType.TRADE_CONFIRM,
                            quantity,
                            0.0,
                        )
                    )
            else:
                print(f"[DROPPING_OPEN_RESPONSE] order_id {order_id}")
                return
        elif status == "REJECTED":
            if not last_processed_order:
                if not in_progress_order:
                    print(
                        f"[DROPPING_REJECTED_RESPONSE] order_id {order_id} not in memory"
                    )
                    return
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.NEW_ORDER_REJECT, 0, 0.0)
                    )
            else:
                if not in_progress_order:
                    print(f"[UNEXPECTED_REJECTED_RESPONSE] order_id {order_id}")
                    return
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.MOD_ORDER_REJECT, 0, 0.0)
                    )
        elif status == "CANCELLED":
            responses.append((QuantplayExchangeResponseType.CANCEL_ORDER_CONFIRM, 0, 0.0))
        elif status == "TRIGGER PENDING":
            if not last_processed_order:
                if not in_progress_order:
                    print(
                        f"[DROPPING_TRIGGER_PENDING_RESPONSE] order_id {order_id} not in memory"
                    )
                    return
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.TRIGGER_CONFIRM, 0, 0.0)
                    )
            else:
                print(
                    f"[DROPPING_TRIGGER_PENDING_RESPONSE] order_id {order_id} already in last_processed map"
                )
                return
        else:
            print(f"[ZERODHA_UNKNOWN_STATUS] {log_message} full_data {data}")
            return

        for response_type, __quantity, avg_price in responses:
            order_resp = QuantplayExchangeResponse(
                order_id, response_type, __quantity, avg_price, status_message
            )
            super(ZBroker, self).on_order_response(order_resp)

    def is_valid_live_tick(self, tick):
        today_day = datetime.now()
        if tick.exchange in ["NSE", "NFO"]:
            tick_time = tick.last_trade_time
            if (
                (tick_time.hour < 9)
                or (tick_time.hour > 15)
                or (tick_time.day != today_day.day)
                or (tick_time.hour != today_day.hour)
                or (tick_time.minute != today_day.minute)
            ):
                # print("Incorrect Trade time {}".format(tick))
                return False
            elif tick_time.hour == 9 and tick_time.minute < 15:
                self.pre_market_volume[tick.symbol] = tick.volume_traded
                return False
            elif tick_time.hour == 15 and tick_time.minute > 28:
                print("Tick after 15:20 stock {} tick {}".format(tick.symbol, tick))
                return False

            return True

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=8,
    )
    def get_historical_data_from_kite(
        self, instrument, start_date, end_date, interval, continuous=False
    ):
        return self.kite.historical_data(
            instrument, start_date, end_date, interval, continuous=continuous
        )

    def get_historical_data(self, instrument, start_date, end_date):
        data_by_interval = dict()

        for interval in self.tick_intervals:
            if interval == "5minute":
                days_diff = 100
            elif interval == "minute":
                days_diff = 60
            elif interval == "day":
                days_diff = 2000
            else:
                raise Exception("interval {} not whitelisted".format(interval))

            time_diff = timedelta(days=days_diff)

            data = []
            while end_date > (start_date + time_diff):
                print(
                    "querying data from [%s] [%s], instrument [%s] interval [%s]"
                    % (start_date, start_date + time_diff, instrument, interval)
                )
                temp_data = self.get_historical_data_from_kite(
                    instrument,
                    start_date,
                    start_date + time_diff,
                    interval,
                    continuous=False,
                )

                start_date += time_diff

                if temp_data is not None and len(temp_data) > 0:
                    data = data + temp_data

            print(
                "querying data from [%s] [%s] instrument [%s] interval [%s]"
                % (start_date, end_date, instrument, interval)
            )
            temp_data = self.get_historical_data_from_kite(
                instrument, start_date, end_date, interval, continuous=False
            )
            data = data + temp_data
            print("Interval {} Total size {}".format(interval, len(data)))

            df = pd.DataFrame(data)
            if len(df) > 0:
                symbol = self.instrument_id_to_symbol_map[instrument]
                df.loc[:, "symbol"] = symbol
                df.loc[:, "date"] = df["date"].dt.tz_localize(None)
                df.loc[:, "date"] = pd.to_datetime(df.date)

            data_by_interval[interval] = df

        return data_by_interval

    def get_equity_instruments(self, main_instruments):
        stock_list = market.symbols()
        main_instruments = [
            a for a in main_instruments if a["tradingsymbol"] in stock_list
        ]

        indices_instruments = [
            a for a in self.get_instruments() if a["segment"] == "INDICES"
        ]
        main_instruments += indices_instruments

        return main_instruments

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def filter_instruments(self, exchange, segment, name=None):
        main_instruments = self.kite.instruments()

        main_instruments = [a for a in main_instruments if a["exchange"] == exchange]
        main_instruments = [a for a in main_instruments if a["segment"] == segment]

        if name is not None:
            main_instruments = [a for a in main_instruments if name in a["name"]]

        return main_instruments

    def store_data(
        self,
        dataset_path="/NSE_EQ/",
        intervals=["minute", "day"],
        start_date=datetime(2015, 1, 1, 00, 00),
    ):
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
            already_fetched_symbols = ZBroker.get_already_stored_stocks(
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

                            # FileUtils.save_file(data, instrument['tradingsymbol'], interval, dataset_path)
                    except Exception as e:
                        print("[FAILED_TO_FETCH_DATA] [{}] {}".format(symbol, e))
                    bar()
