import copy

import numpy as np
import pandas as pd
from quantplay.utils.transaction_utils import TransactionCost
from quantplay.reporting.visuals import VisualReport

from quantplay.utils.constant import Order, ExchangeName
from quantplay.utils.constant import (
    StrategyMetricsTableColumns,
)


class StrategyReport:
    @staticmethod
    def max_drawdown(vec):
        vec = vec.fillna(method="ffill").fillna(method="bfill")
        maximums = np.maximum.accumulate(vec)
        drawdowns = maximums - vec
        #
        # for i in range(0, 140):
        #     print(vec[i], maximums[i], drawdowns[i])

        return np.max(drawdowns)

    @staticmethod
    def max_drawdown_days(vec):
        start_index = 0
        running_max_balance = 0
        max_drawdown_days = 0
        for i in range(0, len(vec)):
            balance = vec[i]

            if balance > running_max_balance:
                running_max_balance = balance
                start_index = i

            max_drawdown_days = max(max_drawdown_days, i - start_index)

        return max_drawdown_days

    @staticmethod
    def get_sharpe_ratio(portfolio):
        portfolio["today_date"] = pd.to_datetime(portfolio.order_timestamp)
        portfolio["today_date"] = portfolio.today_date.dt.date
        t_df = portfolio.groupby("today_date")["exposure"].sum().reset_index()
        exposure_90 = t_df.exposure.quantile(0.9)

        portfolio["Daily_Returns"] = portfolio.profit / portfolio.exposure

        Sharpe_Ratio = (
            portfolio["Daily_Returns"].mean() / portfolio["Daily_Returns"].std()
        )
        Sharpe_Ratio = Sharpe_Ratio * 100

        portfolio["Date"] = portfolio["order_timestamp"] - pd.to_timedelta(7, unit="d")
        data = (
            portfolio.groupby([pd.Grouper(key="Date", freq="W-MON")])[
                ["profit", "exposure"]
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        data["Daily_Returns"] = data["profit"] / abs(data["exposure"])
        weekly_sharpe_ratio = data["Daily_Returns"].mean() / data["Daily_Returns"].std()
        weekly_sharpe_ratio = weekly_sharpe_ratio * 100

        portfolio["Date"] = portfolio["order_timestamp"]
        monthly_data = (
            portfolio.groupby([pd.Grouper(key="Date", freq="M")])[["profit", "exposure"]]
            .sum()
            .reset_index()
            .sort_values("Date")
        )
        monthly_data["Daily_Returns"] = monthly_data["profit"] / abs(
            monthly_data["exposure"]
        )
        monthly_sharpe_ratio = (
            monthly_data["Daily_Returns"].mean() / monthly_data["Daily_Returns"].std()
        )
        monthly_sharpe_ratio = monthly_sharpe_ratio * 100

        response = {}
        response[StrategyMetricsTableColumns.weekly_sharpe_ratio] = weekly_sharpe_ratio
        response[StrategyMetricsTableColumns.monthly_sharpe_ratio] = monthly_sharpe_ratio
        response[StrategyMetricsTableColumns.sharpe_ratio] = Sharpe_Ratio
        response[StrategyMetricsTableColumns.monthly_pnl] = monthly_data["profit"].mean()
        response[StrategyMetricsTableColumns.exposure_90] = exposure_90

        return response

    @staticmethod
    def print_report(response):
        result = pd.DataFrame(response)
        print(
            result[
                [
                    "year",
                    "bps",
                    "monthly_pnl",
                    "max_drawdown_days",
                    "max_drawdown",
                    "sharpe_ratio",
                    "total_signals",
                    "success_ratio",
                    "exposure_90",
                    "total_profit",
                    "unique_stocks",
                ]
            ]
        )

    @staticmethod
    def print_portfolio(portfolio, tag=None):
        file_prefix = ""
        if tag is not None:
            file_prefix = "{}_".format(tag)

        VisualReport.display_profit_report(
            portfolio, groupby="M", file_prefix=file_prefix
        )
        VisualReport.display_profit_report(
            portfolio, groupby="Y", file_prefix=file_prefix
        )
        VisualReport.display_balance_report(portfolio, file_prefix=file_prefix)

    @staticmethod
    def add_more_params(portfolio, cm_slippage=0, fno_slippage=0):
        # Basic trade checks
        portfolio = portfolio[portfolio.close_price > 0]
        portfolio = portfolio[portfolio.entry_price > 0]

        portfolio.loc[:, "order_timestamp"] = pd.to_datetime(portfolio["order_timestamp"])
        portfolio.loc[:, "order_timestamp"] = portfolio.sort_values("order_timestamp")

        portfolio.loc[:, "profit"] = portfolio.exposure * (
            1 - portfolio.close_price / portfolio.entry_price
        )

        portfolio.loc[:, Order.profit] = np.where(
            portfolio[Order.transaction_type] == Order.sell_transaction,
            portfolio.profit,
            -portfolio.profit,
        )

        portfolio = TransactionCost.add_transaction_costs(portfolio)
        portfolio.loc[:, Order.profit] = portfolio.profit - portfolio.total_charges
        portfolio.loc[:, Order.profit] = np.where(
            portfolio.exchange == ExchangeName.nse,
            portfolio.profit - portfolio.exposure * cm_slippage,
            portfolio.profit - portfolio.exposure * fno_slippage,
        )

        portfolio.loc[:, "pct_profit"] = portfolio.profit / portfolio.exposure

        portfolio.loc[:, "day_of_week"] = portfolio.order_timestamp.dt.day_name()
        portfolio.loc[:, "point_diff"] = np.where(
            portfolio[Order.transaction_type] == Order.sell_transaction,
            portfolio.entry_price - portfolio.close_price,
            portfolio.close_price - portfolio.entry_price,
        )

        portfolio.loc[:, "option_type"] = np.where(
            portfolio["tradingsymbol"].str.contains("PE"), "PE", "CE"
        )

        return portfolio

    @staticmethod
    def create_report_by_df(portfolio, cm_slippage=0, fno_slippage=0):
        portfolio = StrategyReport.add_more_params(portfolio, cm_slippage, fno_slippage)

        portfolio.loc[:, "order_timestamp"] = pd.to_datetime(portfolio["order_timestamp"])
        portfolio.loc[:, "order_timestamp"] = portfolio.sort_values("order_timestamp")

        portfolio.loc[:, "balance"] = portfolio.profit.cumsum()

        portfolio = portfolio.reset_index(drop=True)

        tag = portfolio["tag"].iat[0]

        portfolio["year"] = portfolio.order_timestamp.dt.year
        years = portfolio["year"].unique()

        response = StrategyReport.create_single_report(copy.deepcopy(portfolio))
        response[StrategyMetricsTableColumns.tag] = tag
        response["year"] = "ALL"

        response_list = []
        response_list.append(copy.deepcopy(response))

        for i in range(0, len(years)):
            year = int(years[i])
            data = portfolio[portfolio.year == year]
            response = StrategyReport.create_single_report(data)
            response[StrategyMetricsTableColumns.tag] = tag
            response["year"] = year
            response_list.append(copy.deepcopy(response))
        return response_list

    @staticmethod
    def create_report(strategy_params):
        input = strategy_params
        strategy_params = {}
        strategy_params[StrategyMetricsTableColumns.tag] = input["tag"]
        portfolio = pd.read_csv("/tmp/{}.csv".format(strategy_params["tag"]))

        return StrategyReport.create_report_by_df(portfolio)

    @staticmethod
    def create_single_report(portfolio):
        response = {}
        portfolio = portfolio.sort_values("order_timestamp")

        response["total_profit"] = portfolio["profit"].sum()

        portfolio.loc[:, "balance"] = portfolio.profit.cumsum()

        portfolio.loc[:, "date"] = portfolio.order_timestamp.dt.date

        # unique stock count
        t_df = portfolio.groupby("date").symbol.nunique().reset_index()
        response[StrategyMetricsTableColumns.unique_stocks] = int(t_df.symbol.mean())

        day_wise_pnl = portfolio.groupby(["date"])["profit"].sum().reset_index()
        day_wise_pnl = day_wise_pnl.sort_values("date")

        day_wise_pnl.loc[:, "is_loss"] = np.where(day_wise_pnl.profit > 0, 0, 1)
        m = day_wise_pnl.is_loss.astype(bool)
        day_wise_pnl.loc[:, "loss_streak"] = (
            m.groupby([m, (~m).cumsum().where(m)]).cumcount().add(1).mul(m)
        )

        day_wise_pnl.loc[:, "is_win"] = np.where(day_wise_pnl.profit > 0, 1, 0)
        m = day_wise_pnl.is_win.astype(bool)
        day_wise_pnl.loc[:, "win_streak"] = (
            m.groupby([m, (~m).cumsum().where(m)]).cumcount().add(1).mul(m)
        )

        day_wise_pnl.loc[:, "balance"] = day_wise_pnl.profit.cumsum()
        max_drawdown = StrategyReport.max_drawdown(day_wise_pnl["balance"])
        max_drawdown_days = StrategyReport.max_drawdown_days(day_wise_pnl["balance"])

        sharpe_response = StrategyReport.get_sharpe_ratio(portfolio)

        response[StrategyMetricsTableColumns.max_drawdown] = "{}".format(max_drawdown)
        response[StrategyMetricsTableColumns.max_drawdown_days] = "{}".format(
            max_drawdown_days
        )
        response[StrategyMetricsTableColumns.max_gain] = portfolio["profit"].max()
        response[StrategyMetricsTableColumns.max_loss] = portfolio["profit"].min()
        response[StrategyMetricsTableColumns.lossing_streak] = int(
            day_wise_pnl.loss_streak.max()
        )
        response[StrategyMetricsTableColumns.winning_streak] = int(
            day_wise_pnl.win_streak.max()
        )

        for key in sharpe_response:
            response[key] = sharpe_response[key]

        profit_trade = portfolio[portfolio.profit > 0]
        lossing_trade = portfolio[portfolio.profit < 0]

        response[StrategyMetricsTableColumns.avg_profit] = profit_trade["profit"].mean()
        response[StrategyMetricsTableColumns.avg_loss] = lossing_trade["profit"].mean()

        response["number_of_losses"] = len(lossing_trade)
        response["number_of_wins"] = len(profit_trade)
        response["total_signals"] = len(portfolio)
        response["total_trading_days"] = len(portfolio.order_timestamp.dt.date.unique())
        response["drawdown_pnl_ratio"] = (
            float(response["max_drawdown"]) / response["monthly_pnl"]
        )
        response["success_ratio"] = response["number_of_wins"] / (
            response["number_of_losses"] + response["number_of_wins"]
        )
        response["avg_pnl"] = portfolio["profit"].mean()

        response["bps"] = (
            portfolio["profit"].sum() / portfolio["exposure"].sum()
        ) * 10000

        return response


if __name__ == "__main__":
    strategy_params = {"tag": "matsya"}

    pass
