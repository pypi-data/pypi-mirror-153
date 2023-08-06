import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import copy


class VisualReport:
    @staticmethod
    def display_profit_report(trades, groupby="M", file_prefix=""):
        """Saves profit report and displays it.

        :param: groupby: M for monthly, Y for yearly, W for weekly
        """

        groupby_filter_to_str_mapper = {"M": "Month", "Y": "Year", "W": "Week"}

        file_path = "/tmp/{}profit_return_grouped_by_{}.png".format(
            file_prefix, groupby_filter_to_str_mapper[groupby]
        )
        df = (
            trades.groupby([pd.Grouper(key="order_timestamp", freq=groupby)])["profit"]
            .sum()
            .reset_index()
        )
        df.loc[:, "order_timestamp"] = df.order_timestamp.dt.date.astype(str)
        sns.set(rc={"figure.figsize": (11.7, 8.27)})
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x="order_timestamp", y="profit", data=df).set(
            title="Profit by {}".format(groupby_filter_to_str_mapper[groupby])
        )
        plt.xticks(rotation=90)
        plt.savefig(file_path)
        plt.show()

    @staticmethod
    def display_balance_report(trades, file_prefix):
        file_path = "/tmp/{}balance.png".format(file_prefix)
        trades.loc[:, "balance"] = trades.sort_values(["order_timestamp"]).profit.cumsum()
        trades.plot(kind="line", x="date", y="balance", color="blue")
        plt.title("Balance Progression")
        plt.savefig(file_path)
        plt.show()
