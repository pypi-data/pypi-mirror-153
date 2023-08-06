from quantplay.utils.constant import Order, StrategyType, ExchangeName
import numpy as np
import pandas as pd


class TransactionCost:

    ZERODHA_BROKERAGE_CHARGES = 20

    @staticmethod
    def add_transaction_costs(orders_df):
        """
        https://zerodha.com/charges/#tab-equities
        """
        orders_df.loc[:, Order.order_timestamp] = pd.to_datetime(
            orders_df.order_timestamp
        )
        orders_df.loc[:, Order.closing_timestamp] = pd.to_datetime(
            orders_df.closing_timestamp
        )

        orders_df.loc[:, Order.is_intraday] = np.where(
            orders_df.strategy_type == StrategyType.intraday,
            True,
            False,
        )

        orders_df.loc[:, Order.sell_side_price] = np.where(
            orders_df[Order.transaction_type] == Order.sell_transaction,
            orders_df[Order.entry_price],
            orders_df[Order.close_price],
        )
        orders_df.loc[:, Order.buy_side_price] = np.where(
            orders_df[Order.transaction_type] == Order.buy_transaction,
            orders_df[Order.entry_price],
            orders_df[Order.close_price],
        )

        orders_df.loc[:, Order.combined_exposure] = (
            orders_df[Order.sell_side_price] + orders_df[Order.buy_side_price]
        ) * orders_df[Order.quantity]

        if "exchange" not in orders_df.columns:
            orders_df.loc[:, "exchange"] = ExchangeName.nse

        charges_condition = [
            (orders_df[Order.is_intraday] == True)
            & (orders_df["exchange"] == ExchangeName.nse),
            (orders_df[Order.is_intraday] == False)
            & (orders_df["exchange"] == ExchangeName.nse),
            (orders_df["exchange"] == ExchangeName.nfo)
            & (orders_df["security_type"] == "FUT"),
            (orders_df["exchange"] == ExchangeName.nfo)
            & (orders_df["security_type"] == "OPT"),
        ]

        brokerage_charges_choices = [
            0.0003 * orders_df[Order.combined_exposure],
            0,
            40,
            40,
        ]

        orders_df.loc[:, Order.brokerage_charges] = np.select(
            charges_condition, brokerage_charges_choices, default=0
        )

        stt_charges_choices = [
            0.00025 * (orders_df[Order.sell_side_price] * orders_df[Order.quantity]),
            0.001 * orders_df[Order.combined_exposure],
            0.0001 * (orders_df[Order.sell_side_price] * orders_df[Order.quantity]),
            0.0005 * (orders_df[Order.sell_side_price] * orders_df[Order.quantity]),
        ]

        orders_df.loc[:, Order.stt_charges] = np.select(
            charges_condition, stt_charges_choices, default=0
        )

        exchange_charges_choices = [
            0.0000345 * orders_df[Order.combined_exposure],
            0.0000345 * orders_df[Order.combined_exposure],
            0.00002 * orders_df[Order.combined_exposure],
            0.00053 * orders_df[Order.combined_exposure],
        ]

        orders_df.loc[:, Order.exchange_transaction_charges] = np.select(
            charges_condition, exchange_charges_choices, default=0
        )

        stamp_charges_choices = [
            0.00003 * orders_df[Order.buy_side_price] * orders_df[Order.quantity],
            0.00015 * orders_df[Order.buy_side_price] * orders_df[Order.quantity],
            0.00002 * orders_df[Order.buy_side_price] * orders_df[Order.quantity],
            0.00003 * orders_df[Order.buy_side_price] * orders_df[Order.quantity],
        ]

        orders_df.loc[:, Order.stamp_charges] = np.select(
            charges_condition, stamp_charges_choices, default=0
        )

        orders_df.loc[:, Order.gst_charges] = (
            0.18 * orders_df[Order.exchange_transaction_charges]
        )

        orders_df.loc[:, Order.total_charges] = (
            orders_df[Order.stt_charges]
            + orders_df[Order.exchange_transaction_charges]
            + orders_df[Order.stamp_charges]
            + orders_df[Order.gst_charges]
            + orders_df[Order.brokerage_charges]
        )

        return orders_df
