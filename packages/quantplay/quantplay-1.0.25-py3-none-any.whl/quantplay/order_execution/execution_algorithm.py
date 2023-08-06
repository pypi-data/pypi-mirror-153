from quantplay.utils.constant import OrderType


class OrderExecutionAlgorithm:
    """Base class to be extended by different execution algorithms
    which can be assigned to different orders and easily A/B tested.
    """

    def __init__(self, max_modification_count, *args, **kwargs):
        """Creates an object of OrderExecutionAlgorithm. When
        max_modification_count number of modifications are done
        to the order, the order is converted to the Market order.

        :param: max_modification_count: int, between [1, 15]
        """

        if (
            not isinstance(max_modification_count, int)
            or max_modification_count < 1
            or max_modification_count > 15
        ):
            raise Exception(
                "Must provide max_modification_count as an int between 1 and 15"
            )

        self.max_modification_count = max_modification_count

    def modify_order(self, last_tick, quantplay_order, is_new_order=False):
        """Modifies the quantplay_order in_place before sending to the
        exchange
        """

        # if quantplay_order.modifications == self.max_modification_count:
        #     quantplay_order.order_type = str(OrderType.market)
        #     return
        quantplay_order.order_type = str(OrderType.market)
        quantplay_order.price = self.get_new_price(
            last_tick, quantplay_order, is_new_order=is_new_order
        )

        quantplay_order.modifications += 1

    def get_new_price(self, last_tick, quantplay_order, is_new_order=False, **kwargs):
        """Sets the price in the quantplay order
        for the next modification
        """
        raise NotImplementedError

    def get_next_modification_time(self, last_tick, quantplay_order):
        """Returns time in seconds after which the quantplay
        order should be modified
        """
        raise NotImplementedError

    def __repr__(self):
        return str(
            {"name": self.name, "max_modification_count": self.max_modification_count}
        )
