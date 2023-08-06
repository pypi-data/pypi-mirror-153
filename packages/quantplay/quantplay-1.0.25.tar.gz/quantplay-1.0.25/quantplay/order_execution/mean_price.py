from quantplay.order_execution.execution_algorithm import (
    OrderExecutionAlgorithm,
)
from quantplay.utils.constant import Constants


class MeanPriceExecutionAlgo(OrderExecutionAlgorithm):
    def __init__(self, max_modification_count, *args, **kwargs):
        self.name = "MeanPriceExecutionAlgo"
        super(MeanPriceExecutionAlgo, self).__init__(max_modification_count)

    def get_new_price(
        self,
        last_tick,
        quantplay_order,
        is_new_order=False,
        buy_side_factor=1,
        sell_side_factor=1,
    ):

        new_price = None

        if is_new_order:
            if quantplay_order.price:
                new_price = quantplay_order.price
            else:
                new_price = last_tick.last_price
        else:
            order_book = last_tick.order_book
            sell_side, buy_side = order_book.sell_side, order_book.buy_side
            new_price = (sell_side[0].price + buy_side[0].price) / 2

        if quantplay_order.transaction_type == "SELL":
            new_price = new_price * sell_side_factor
        else:
            new_price = new_price * buy_side_factor

        return Constants.round_to_tick(new_price)

    def get_next_modification_time(self, last_tick, quantplay_order):
        return 10
