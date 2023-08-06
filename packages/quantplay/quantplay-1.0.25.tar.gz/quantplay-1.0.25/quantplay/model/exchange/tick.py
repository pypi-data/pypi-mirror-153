from typing import NamedTuple, List
from datetime import datetime
from collections import defaultdict


class BookRecord(NamedTuple):
    price: float
    orders: int
    quantity: int

    @classmethod
    def from_zerodha_book_record(cls, zerodha_book_record_dict):
        """Returns BookRecord from book record present in depth
        field of zerodha tick
        """
        d = zerodha_book_record_dict
        return cls(d["price"], d["orders"], d["quantity"])


class OrderBook(NamedTuple):
    sell_side: List[BookRecord]
    buy_side: List[BookRecord]

    @classmethod
    def from_zerodha_depth(cls, zerodha_depth_dict):
        """Creates OrderBook from Zerodha Depth Dict
        received in the tick data
        """
        d = zerodha_depth_dict
        sell_depth = d["sell"]
        buy_depth = d["buy"]

        sell_side_book = [BookRecord.from_zerodha_book_record(r) for r in sell_depth]
        buy_side_book = [BookRecord.from_zerodha_book_record(r) for r in buy_depth]

        return cls(sell_side_book, buy_side_book)


class QuantplayTick(NamedTuple):
    exchange: str
    instrument_id: int
    symbol: str
    tradable: bool
    last_trade_time: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    oi: int
    oi_day_high: int
    oi_day_low: int
    volume_traded: int
    last_price: float
    average_traded_price: float
    last_traded_quantity: int
    total_buy_quantity: int
    total_sell_quantity: int
    order_book: OrderBook

    @classmethod
    def from_zerodha_tick(
        cls,
        zerodha_tick_dict,
        instrument_id_to_symbol_map,
        instrument_id_to_exchange_map,
    ):
        """Creates QuantplayTick from tick returned by zerodha API"""

        d = zerodha_tick_dict
        instrument_id = d["instrument_token"]
        symbol = instrument_id_to_symbol_map[instrument_id]
        exchange = instrument_id_to_exchange_map[instrument_id]

        order_book = None
        if "depth" in d:
            order_book = OrderBook.from_zerodha_depth(d["depth"])

        if "last_trade_time" in d:
            last_trade_time = d["last_trade_time"]
        else:
            last_trade_time = d["exchange_timestamp"]

        dd = defaultdict(float, d)

        return cls(
            exchange,
            instrument_id,
            symbol,
            dd["tradable"],
            last_trade_time,
            dd["ohlc"]["open"],
            dd["ohlc"]["high"],
            dd["ohlc"]["low"],
            dd["ohlc"]["close"],
            dd["oi"],
            dd["oi_day_high"],
            dd["oi_day_low"],
            dd["volume_traded"],
            dd["last_price"],
            dd["average_traded_price"],
            dd["last_traded_quantity"],
            dd["total_buy_quantity"],
            dd["total_sell_quantity"],
            order_book,
        )
