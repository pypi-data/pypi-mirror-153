from quantplay.utils.constant import (
    Product,
    OrderType,
    OrderVariety,
    Order,
    ExchangeName,
    StrategyType,
)
import pandas as pd
import copy
from enum import Enum
from typing import NamedTuple
from quantplay.utils.constant import Constants


class QuantplayTransactionStatus(Enum):
    IN_PROGRESS = 1  # Current QuantplayExchangeOrder sent for execution is in progress and no response is received yet.
    PROCESSED = 2  # A response has been received for the sent QuantplayExchangeOrder


class QuantplayExchangeResponseType(Enum):

    NEW_ORDER_CONFIRM = 1
    NEW_ORDER_REJECT = 2
    MOD_ORDER_CONFIRM = 3
    MOD_ORDER_REJECT = 4
    TRADE_CONFIRM = 5
    OMS_REJECT = 6
    RMS_REJECT = 7
    CANCEL_ORDER_CONFIRM = 8
    TRIGGER_CONFIRM = 9


class QuantplayExchangeOrderStatus(Enum):
    OPEN = 1
    COMPLETE = 2
    REJECTED = 3
    CANCELLED = 4

    @classmethod
    def from_response_type(cls, response_type: QuantplayExchangeResponseType):

        if response_type in [
            QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
            QuantplayExchangeResponseType.MOD_ORDER_CONFIRM,
            QuantplayExchangeResponseType.MOD_ORDER_REJECT,
            QuantplayExchangeResponseType.TRADE_CONFIRM,
        ]:
            return cls.OPEN
        elif response_type in [
            QuantplayExchangeResponseType.NEW_ORDER_REJECT,
            QuantplayExchangeResponseType.OMS_REJECT,
            QuantplayExchangeResponseType.RMS_REJECT,
        ]:
            return cls.REJECTED
        elif response_type == QuantplayExchangeResponseType.CANCEL_ORDER_CONFIRM:
            return cls.CANCELLED
        else:
            raise Exception(f"Invalid response_type {response_type}")


class QuantplayExchangeOrder:
    @staticmethod
    def get_exchange_orders(
        trades,
        order_type=OrderType.limit,
        exchange=ExchangeName.nse,
        execution_algo=None,
    ):
        all_trades = []
        for trade in trades:
            all_trades.append(
                QuantplayExchangeOrder(
                    trade,
                    order_type=order_type,
                    exchange=exchange,
                    execution_algo=execution_algo,
                )
            )
        return all_trades

    def initialize_basic_fields(self):
        self.is_child_order = False
        self.order_id = None
        self.modifications = -1  # Indicating it's a new order
        self.order_placement_time = None
        self.transaction_status: QuantplayTransactionStatus = None
        self.order_status: QuantplayExchangeOrderStatus = None
        self.filled_quantity = 0
        self.average_price = 0.0

    def __init__(
        self,
        trade,
        order_type=OrderType.limit,
        exchange=ExchangeName.nse,
        execution_algo=None,
    ):

        self.initialize_basic_fields()
        self.execution_algo = execution_algo
        self.order_type = str(order_type)
        self.exchange = exchange

        if "tag" not in trade:
            raise Exception(
                "Tag should be present in trade but not found. Trade: {}".format(trade)
            )
        if "quantity" not in trade:
            raise Exception(
                "Quantity should be present in trade but not found. Trade: {}".format(
                    trade
                )
            )
        if "tradingsymbol" not in trade:
            raise Exception(
                "tradingsymbol should be present in trade but not found. Trade: {}".format(
                    trade
                )
            )
        if "strategy_type" not in trade:
            raise Exception(
                "strategy_type should be present in trade but not found. Trade: {}".format(
                    trade
                )
            )

        self.tag = str(trade["tag"])
        self.quantity = abs(int(trade["quantity"]))
        self.strategy_type = trade["strategy_type"]
        self.tradingsymbol = str(trade["tradingsymbol"])
        self.transaction_type = trade["transaction_type"]

        # TODO CRITICAL
        self.price = None
        self.trigger_price = None
        self.order_timestamp = None

        if "stoploss" in trade:
            self.stoploss = float(trade["stoploss"])
        else:
            self.stoploss = None

        if "price" in trade:
            self.price = Constants.round_to_tick(float(trade["price"]))

        if "squareoff" in trade:
            self.squareoff = float(trade["squareoff"])
        else:
            self.squareoff = None

        if "trigger_price" in trade:
            self.trigger_price = Constants.round_to_tick(float(trade["trigger_price"]))

        if "order_timestamp" in trade:
            self.order_timestamp = trade["order_timestamp"]

        if "lot_size" in trade and not pd.isna(trade["lot_size"]):
            self.lot_size = trade["lot_size"]

    def get_child_order(self):
        """Returns the child order for this QuantplayExchangeOrder"""
        if self.is_child_order:
            raise Exception(f"[ALREADY_CHILD_ORDER] order is already a child. {self}")

        child_order = copy.deepcopy(self)

        child_order.initialize_basic_fields()
        child_order.is_child_order = True
        child_order.order_type = OrderType.sl

        if self.transaction_type == "SELL":
            child_order.transaction_type = "BUY"
            child_order.trigger_price = child_order.price * (1 + child_order.stoploss)
            child_order.price = child_order.trigger_price * 1.03
        else:
            child_order.transaction_type = "SELL"
            child_order.trigger_price = child_order.price * (1 - child_order.stoploss)
            child_order.price = child_order.trigger_price * 0.97

        child_order.price = Constants.round_to_tick(child_order.price)
        child_order.trigger_price = Constants.round_to_tick(child_order.trigger_price)

        return child_order

    def modify_child_order_for_closing(self):
        self.order_type = OrderType.limit

    def to_zerodha_order(self):
        """Translates QuantplayExchangeOrder to zerodha order"""
        data = {}
        data["variety"] = OrderVariety.regular
        data["tradingsymbol"] = self.tradingsymbol
        data["exchange"] = self.exchange
        data["transaction_type"] = self.transaction_type
        data["quantity"] = self.quantity
        data["order_type"] = self.order_type
        data["disclosed_quantity"] = None
        data["price"] = self.price
        data["trigger_price"] = self.trigger_price

        if self.exchange == ExchangeName.nfo:
            data["product"] = Product.nrml
        if (
            self.exchange == ExchangeName.nse
            and self.strategy_type == StrategyType.intraday
        ):
            data["product"] = Product.mis
        if (
            self.exchange == ExchangeName.nse
            and self.strategy_type == StrategyType.overnight
        ):
            data["product"] = Product.cnc

        data["stoploss"] = self.stoploss
        data["tag"] = self.tag
        data["squareoff"] = self.squareoff

        return data

    @staticmethod
    def from_zerodha_order(zerodha_order_dict, is_child_order=False):
        d = zerodha_order_dict
        trade = {}
        trade["tag"] = d["tag"]
        trade["quantity"] = d["quantity"]
        trade["tradingsymbol"] = d["tradingsymbol"]
        trade["transaction_type"] = d["transaction_type"]
        trade["price"] = d["price"]
        trade["trigger_price"] = d["trigger_price"]
        trade["order_timestamp"] = d["order_timestamp"]
        trade["strategy_type"] = None

        order = QuantplayExchangeOrder(
            trade, order_type=d["order_type"], exchange=d["exchange"], execution_algo=None
        )
        order.order_id = d["order_id"]
        order.is_child_order = is_child_order
        return order

    def set_strategy_attributes(self, strategy_obj):
        self.strategy_type = strategy_obj.strategy_type
        self.execution_algo = strategy_obj.execution_algo

    def __repr__(self):
        return str(self.__dict__)


class QuantplayExchangeResponse(NamedTuple):
    order_id: str
    response_type: QuantplayExchangeResponseType
    quantity: int
    average_price: float
    message: str

    def __repr__(self):
        return f"order_id {self.order_id} response_type {self.response_type} quantity {self.quantity} average_price {self.average_price} message {self.message}"
