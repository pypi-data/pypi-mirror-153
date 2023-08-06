import time

import pandas as pd
from retrying import retry

from joblib import Parallel, delayed, parallel_backend
from os import path
import os
from quantplay.utils.constant import Constants, TickInterval, timeit


class DataUtils:
    @staticmethod
    @timeit(MetricName="DataUtils:load_file")
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def load_file(
        interval=None,
        stock=None,
        path=None,
        args=None,
        columns=None,
        ignore_if_not_found=False,
        **kwargs
    ):
        path = path + "/" + stock + ".csv"

        df = None
        try:
            Constants.logger.info("loading {}".format(path))
            df = pd.read_csv(path, usecols=columns)

            if "after" in kwargs:
                df = df[df.date >= kwargs["after"]]
            if "before" in kwargs:
                df = df[df.date <= kwargs["before"]]

            Constants.logger.info("loaded {}".format(path))
            df = df.reset_index(drop=True)
            return df
            # x = pd.read_csv(path)
        except Exception as e:
            Constants.logger.error(
                "Failed to load {}/{}.csv Got {}".format(interval, stock, e)
            )
            if ignore_if_not_found:
                return pd.DataFrame()
            raise e

    @staticmethod
    @timeit(MetricName="DataUtils:load_data_using_pandas")
    def load_data_using_pandas(
        stocks=None,
        interval=None,
        path=None,
        columns=None,
        args=None,
        is_map=False,
        ignore_if_not_found=False,
        **kwargs
    ):
        start_time = time.time()
        response = {}
        if path == None:
            path = Constants.stock_data_path + interval
        else:
            path = path + interval

        response = Parallel(n_jobs=4)(
            delayed(DataUtils.load_file)(
                interval=interval,
                stock=stock,
                path=path,
                columns=columns,
                args=args,
                ignore_if_not_found=ignore_if_not_found,
                **kwargs
            )
            for stock in stocks
        )

        # CandleUtils.candle_count_check_v2(response)
        print(
            "time taken to load data for {} candles --- {} seconds ---".format(
                interval, time.time() - start_time
            )
        )

        response = pd.concat(response).reset_index(drop=True)
        response.loc[:, "date"] = pd.to_datetime(response.date)
        response.loc[:, "open"] = response.open.astype(float)
        response.loc[:, "high"] = response.high.astype(float)
        response.loc[:, "low"] = response.low.astype(float)
        response.loc[:, "close"] = response.close.astype(float)
        response.loc[:, "volume"] = response.volume.astype(float)

        return response

    @staticmethod
    @timeit(MetricName="DataUtils:midday_data_merge_v3")
    def midday_data_merge(
        day_candle_data,
        candle_data,
        timing_value=None,
        columns_to_retrieve=["close", "high", "volume"],
    ):
        hour, minute = timing_value.split(":")
        hour = int(hour)
        minute = int(minute)

        time_df = candle_data[
            (candle_data.date.dt.hour == hour) & (candle_data.date.dt.minute == minute)
        ]

        assert len(time_df) > 0

        for column in columns_to_retrieve:
            time_df.loc[:, "tick_{}".format(column)] = time_df[column]
        columns_to_retrieve = ["tick_{}".format(a) for a in columns_to_retrieve]

        columns_to_drop = columns_to_retrieve
        columns_to_drop = [a for a in columns_to_drop if a in day_candle_data.columns]
        day_candle_data = day_candle_data.drop(columns_to_drop, axis=1)
        day_candle_data = pd.merge(
            day_candle_data,
            time_df[["symbol", "date_only"] + columns_to_retrieve],
            how="left",
            left_on=["date_only", "symbol"],
            right_on=["date_only", "symbol"],
        )

        return day_candle_data

    @staticmethod
    @timeit(MetricName="DataUtils:midday_data_merge_v2")
    def midday_data_merge_v2(day_candle_data, candle_data, columns_to_retrieve=["close"]):

        for column in columns_to_retrieve:
            candle_data.loc[:, "tick_{}".format(column)] = candle_data[column]
        columns_to_retrieve = ["tick_{}".format(a) for a in columns_to_retrieve]

        columns_to_drop = columns_to_retrieve
        columns_to_drop = [a for a in columns_to_drop if a in day_candle_data.columns]
        day_candle_data = day_candle_data.drop(columns_to_drop, axis=1)
        day_candle_data = pd.merge(
            day_candle_data,
            candle_data[["symbol", "date"] + columns_to_retrieve],
            how="left",
            left_on=["tick_timestamp", "symbol"],
            right_on=["date", "symbol"],
        )

        return day_candle_data

    @staticmethod
    @timeit(MetricName="DataUtils:get_data")
    def get_data(path=None, interval=None, stocks=None):
        return DataUtils.load_data_using_pandas(
            stocks=stocks, interval=interval, path=path
        )


if __name__ == "__main__":
    pass
