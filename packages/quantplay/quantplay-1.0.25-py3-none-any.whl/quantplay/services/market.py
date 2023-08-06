from quantplay.utils.data_utils import DataUtils
import requests
import json
from quantplay.utils.config_util import QuantplayConfig
import pandas as pd
import numpy as np
from quantplay.exception.exceptions import AccessDeniedException
from quantplay.utils.exchange import Market as MarketConstants
import copy
from datetime import timedelta
from os.path import expanduser
import re


class Market:
    GET_SYMBOLS_URL = (
        "https://7tpcay1yyk.execute-api.ap-south-1.amazonaws.com/prod/get_symbols"
    )
    EXPIRY_DATA_URL = (
        " https://7tpcay1yyk.execute-api.ap-south-1.amazonaws.com/prod/nearest_expiry"
    )

    def __init__(self):
        config = QuantplayConfig.get_config()
        self.nse_equity_path = "{}/.quantplay/NSE_EQ/".format(expanduser("~"))
        self.nse_opt_path = "{}/.quantplay/NSE_OPT/".format(expanduser("~"))
        self.nse_fut_path = "{}/.quantplay/NSE_FUT/".format(expanduser("~"))

        if "DEFAULT" in config and "nse_equity_path" in config["DEFAULT"]:
            self.nse_equity_path = config["DEFAULT"]["nse_equity_path"]
        if "DEFAULT" in config and "nse_opt_path" in config["DEFAULT"]:
            self.nse_opt_path = config["DEFAULT"]["nse_opt_path"]
        if "DEFAULT" in config and "nse_fut_path" in config["DEFAULT"]:
            self.nse_fut_path = config["DEFAULT"]["nse_fut_path"]

    def get_nearest_expiry_data(
        self,
        symbols=[],
        days_offset=0,
        security_type=None,
        depth=None,
        after_date=None,
        before_date=None,
    ):
        credentials = QuantplayConfig.get_credentials()
        if "DEFAULT" not in credentials or "access_token" not in credentials["DEFAULT"]:
            raise AccessDeniedException(
                "Access Denied, please signin using [quantplay user signin]"
            )

        access_token = credentials["DEFAULT"]["access_token"]
        input = {
            "access_token": access_token,
            "days_offset": days_offset,
        }

        if symbols:
            input["symbols"] = symbols
        if security_type:
            input["security_type"] = security_type
        if depth is not None:
            input["depth"] = depth

        x = requests.post(Market.EXPIRY_DATA_URL, data=json.dumps(input))
        response = json.loads(x.text)

        if "error" in response and response["error"] == True:
            print(response["message"])
            exit(1)

        data = pd.DataFrame(response["data"])

        # TODO Move after date to API input
        if after_date is not None:
            data = data[data.date >= after_date]
        if before_date is not None:
            data = data[data.date <= before_date]
        return data

    def add_expiry(
        self, data, security_type=None, security_expiry_data=None, days_offset=0
    ):
        columns_to_be_added = ["expiry_date", "strike_spread"]

        for column in columns_to_be_added:
            if column in data.columns:
                data = data.drop([column], axis=1)

        symbols = [
            MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP.get(symbol, symbol)
            for symbol in data.symbol.unique()
        ]

        if security_expiry_data is not None and len(security_expiry_data) > 0:
            expiry_data = security_expiry_data
        else:
            expiry_data = self.get_nearest_expiry_data(
                symbols=symbols,
                security_type=security_type,
                days_offset=days_offset,
            )

        data.loc[:, "date_only"] = pd.to_datetime(data.date.dt.date)
        expiry_data.loc[:, "expiry_date"] = pd.to_datetime(expiry_data.expiry_date)
        expiry_data.loc[:, "date_only"] = pd.to_datetime(expiry_data.date)

        for (
            idx_derivative_symbol,
            idx_symbol,
        ) in MarketConstants.DERIVATIVE_SYMBOL_TO_INDEX_SYMBOL_MAP.items():
            expiry_data.loc[:, "symbol"] = expiry_data["symbol"].replace(
                [idx_derivative_symbol], idx_symbol
            )

        data = pd.merge(
            data,
            expiry_data[["date_only", "symbol", "expiry_date", "strike_gap"]],
            how="left",
            left_on=["symbol", "date_only"],
            right_on=["symbol", "date_only"],
        )
        return data

    def symbols(self, universe=None):
        input = {}
        if universe != None:
            input["universe"] = universe

        x = requests.post(Market.GET_SYMBOLS_URL, data=json.dumps(input))
        return json.loads(x.text)

    def option_symbol(self, trade_data, price_column=None, option_type=None):
        trades = copy.deepcopy(trade_data)

        trades.loc[:, "tradingsymbol"] = trades["symbol"].replace(
            MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP
        )
        trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + trades[
            "expiry_date"
        ].dt.strftime("%y").astype(str)

        trades.loc[:, "month_number"] = (
            trades["expiry_date"].dt.strftime("%m").astype(int).astype(str)
        )
        trades.loc[:, "monthly_option_prefix"] = (
            trades["expiry_date"].dt.strftime("%b").str.upper()
        )

        trades.loc[:, "week_option_prefix"] = np.where(
            trades.month_number.astype(int) >= 10,
            trades.monthly_option_prefix.str[0]
            + trades["expiry_date"].dt.strftime("%d").astype(str),
            trades.month_number + trades["expiry_date"].dt.strftime("%d").astype(str),
        )

        trades.loc[:, "next_expiry"] = trades.expiry_date + pd.DateOffset(days=7)

        trades.loc[:, "tradingsymbol"] = np.where(
            trades.expiry_date.dt.month != trades.next_expiry.dt.month,
            trades.tradingsymbol + trades.monthly_option_prefix,
            trades.tradingsymbol + trades.week_option_prefix,
        )

        trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + trades[
            price_column
        ].astype(str)
        if option_type is not None:
            trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + option_type
        else:
            trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + trades.option_type

        trades.loc[:, "security_type"] = "OPT"

        trades = trades.drop(
            [
                "next_expiry",
                "week_option_prefix",
                "monthly_option_prefix",
                "month_number",
            ],
            axis=1,
        )
        return trades

    @staticmethod
    def filter_contracts_matching_expiry_date(option_data):
        if "expiry_date" not in option_data.columns:
            raise Exception("expiry_date column required in option_data")

        if "symbol" not in option_data.columns:
            raise Exception("symbol column required in option_data")

        return option_data[
            option_data.apply(
                lambda x: x["symbol"].startswith(
                    MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[
                        x["equity_symbol"]
                    ]
                    + Market.format_expiry_date(x["expiry_date"], "OPT")
                ),
                axis=1,
            )
        ]

    @staticmethod
    def add_columns_in_option_data(option_data, columns=[]):
        def get_strike_price(x):
            try:
                return int(
                    x["symbol"].split(
                        MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[
                            x["equity_symbol"]
                        ]
                        + Market.format_expiry_date(x["expiry_date"], "OPT")
                    )[1][:-2]
                )
            except Exception as e:
                print(x)
                raise e

        columns_supported = ["equity_symbol", "strike_price", "option_type"]
        if not set(columns).issubset(columns_supported):
            raise Exception(
                f"supports only addition of columns {columns_supported}, but received {columns}"
            )

        for col in columns:
            if col == "equity_symbol":
                option_data.loc[:, "equity_symbol"] = option_data.symbol.apply(
                    lambda x: MarketConstants.DERIVATIVE_SYMBOL_TO_INDEX_SYMBOL_MAP[
                        re.findall("([a-zA-Z]*)\d*.*", x)[0]
                    ]
                )
            elif col == "strike_price":
                option_data.loc[:, "strike_price"] = option_data[
                    ["date", "expiry_date", "symbol", "equity_symbol"]
                ].apply(
                    lambda x: get_strike_price(x),
                    axis=1,
                )

            elif col == "option_type":
                option_data.loc[:, "option_type"] = option_data.symbol.apply(
                    lambda x: x[-2:]
                )

    @staticmethod
    def format_expiry_date(expiry_date, security_type):
        formatted_date = expiry_date.strftime("%y")
        month_number, month_name, day = (
            expiry_date.month,
            expiry_date.strftime("%b").upper(),
            expiry_date.strftime("%d"),
        )

        if security_type == "FUT":
            formatted_date += month_name
        elif security_type == "OPT":
            if month_number >= 10:
                week_prefix = month_name[0] + day
            else:
                week_prefix = str(month_number) + day

            next_expiry = expiry_date + timedelta(days=7)
            if next_expiry.month == expiry_date.month:
                formatted_date += week_prefix
            else:
                formatted_date += month_name
        else:
            raise Exception(
                "Invalid security_type {}. Date argument was {}".format(
                    security_type, expiry_date
                )
            )

        return formatted_date

    def equity_data(self, interval=None, symbols=None):
        df = DataUtils.load_data_using_pandas(
            stocks=symbols, interval=interval, path=self.nse_equity_path
        )
        df.loc[:, "security_type"] = "EQ"
        return df

    def data(self, interval=None, symbols_by_security_type=None, **kwargs):
        security_type_data_path = {
            "EQ": self.nse_equity_path,
            "FUT": self.nse_fut_path,
            "OPT": self.nse_opt_path,
        }
        dfs = []
        for security_type, symbols in symbols_by_security_type.items():

            print(
                f"Loading {security_type} data for {len(set(symbols))} symbols, interval {interval}"
            )
            df = DataUtils.load_data_using_pandas(
                stocks=symbols,
                interval=interval,
                path=security_type_data_path[security_type],
                ignore_if_not_found=True,
                **kwargs,
            )
            df.loc[:, "security_type"] = security_type
            dfs.append(df)

        return pd.concat(dfs, axis=0)

    def options_data(self, interval=None, symbols=None):
        df = DataUtils.load_data_using_pandas(
            stocks=symbols, interval=interval, path=self.nse_opt_path
        )
        df.loc[:, "security_type"] = "OPT"
        return df

    def future_data(self, interval=None, symbols=None):
        df = DataUtils.load_data_using_pandas(
            stocks=symbols, interval=interval, path=self.nse_fut_path
        )
        df.loc[:, "security_type"] = "FUT"
        return df

    def get_trades(self, data, entry_time):
        return data[
            data.assign(Time=data["date"].dt.time.astype(str))["Time"].str.match(
                entry_time
            )
        ]

    @staticmethod
    def merge_price(
        trades,
        data,
        time=None,
        column_name=None,
        merge_on_columns=["symbol", "date_only"],
    ):
        filter_data = data[
            data.assign(Time=data["date"].dt.time.astype(str))["Time"].str.match(time)
        ]

        filter_data.loc[:, column_name] = filter_data.close
        trades = pd.merge(
            trades,
            filter_data[[column_name] + merge_on_columns],
            how="left",
            left_on=merge_on_columns,
            right_on=merge_on_columns,
        )

        return trades

    @staticmethod
    def add_intraday_metrics(data, entry_time, exit_time):
        data.loc[:, "intraday_high"] = data.high
        data.loc[:, "intraday_low"] = data.low

        condition = (data.date.dt.time <= pd.to_datetime(entry_time).time()) | (
            data.date.dt.time > pd.to_datetime(exit_time).time()
        )
        data.loc[:, "intraday_high"] = np.where(condition, np.nan, data.intraday_high)
        data.loc[:, "intraday_low"] = np.where(condition, np.nan, data.intraday_low)

        data.loc[:, "date_only"] = data.date.dt.date
        data.loc[:, "intraday_high"] = data.groupby(
            ["symbol", "date_only"]
        ).intraday_high.transform(max)
        data.loc[:, "intraday_low"] = data.groupby(
            ["symbol", "date_only"]
        ).intraday_low.transform(min)
