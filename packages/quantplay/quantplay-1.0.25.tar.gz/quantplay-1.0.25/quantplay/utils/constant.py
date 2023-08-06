import logging
import os
import decimal
import inspect
import boto3
from functools import wraps
from os.path import expanduser
import psutil, time
import numpy as np
from ec2_metadata import ec2_metadata
import json
import pytz
from datetime import datetime
from typing import NamedTuple

india_tz = pytz.timezone("Asia/Kolkata")

formatter = logging.Formatter(
    "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
)


class ConfigKeys:
    use_firefox_for_kite_token = "use_firefox_for_kite_token"
    tradeview_username = "tradeview_username"
    tradeview_password = "tradeview_password"
    kite_api_key = "kite_api_key"
    kite_api_secret = "kite_api_secret"
    kite_username = "kite_username"
    kite_pin = "kite_pin"
    kite_password = "kite_password"
    kite_left_eye = "kite_left_eye"
    kite_fav_dish = "kite_fav_dish"
    kite_spouse_email = "kite_spouse_email"
    kite_tv = "kite_tv"
    kite_car_color = "kite_car_color"


class ConstString:
    base_path = (
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))).split(
            "AlphaPlayground"
        )[0]
        + "AlphaPlayground"
    )


class LoggerUtils:
    @staticmethod
    def get_log_file_path(file_name):
        today_date = datetime.now()

        return "/tmp/" + file_name + "-" + today_date.strftime("%Y-%m-%d:01") + ".log"

    @staticmethod
    def setup_logger(logger_name, log_file, level=logging.DEBUG):
        log_file = LoggerUtils.get_log_file_path(log_file)
        """Function setup as many loggers as you want"""

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
        logger.disabled = False

        return logger


class IntervalAttribute:
    seconds = "seconds"
    mod_value = "mod_value"


class TickInterval:
    """ToDo: Make Enum"""

    five_minute = "5minute"
    day = "day"
    thirty_minute = "30minute"
    three_minute = "3minute"
    minute = "minute"

    @staticmethod
    def get_interval_seconds(interval: str) -> int:
        if interval == TickInterval.minute:
            return 60
        elif interval == TickInterval.five_minute:
            return 300
        elif interval == TickInterval.three_minute:
            return 180
        elif interval == TickInterval.day:
            return 375 * 60
        elif interval == TickInterval.thirty_minute:
            return 30 * 60
        else:
            raise Exception("Interval {} is not defined".format(interval))


class Constants:
    interval_attributes = {
        TickInterval.minute: {
            IntervalAttribute.seconds: 60,
            IntervalAttribute.mod_value: 1,
        },
        TickInterval.five_minute: {
            IntervalAttribute.seconds: 300,
            IntervalAttribute.mod_value: 5,
        },
        TickInterval.day: {
            IntervalAttribute.seconds: 375 * 60,
            IntervalAttribute.mod_value: 1,
        },
        TickInterval.thirty_minute: {IntervalAttribute.seconds: 30 * 60},
        TickInterval.three_minute: {
            IntervalAttribute.seconds: 180,
            IntervalAttribute.mod_value: 3,
        },
    }

    security_wise_delivery_position = "security_wise_delivery_position"
    daily_volatility = "daily-volatility"
    daily_indices = "daily-indices"
    open_interest = "open-interest"
    combined_open_interest = "combined-open-interest"
    fo_bhavcopy = "fo-bhavcopy"
    cm_bhavcopy = "cm-bhavcopy"
    execution_algorithm = "execution_algorithm"

    close_all_tags = "close_all_tags"
    not_tradable_stocks = []

    nifty_fifty = [
        "M&M",
        "TATASTEEL",
        "ULTRACEMCO",
        "BAJFINANCE",
        "HINDALCO",
        "VEDL",
        "JSWSTEEL",
        "EICHERMOT",
        "ADANIPORTS",
        "GRASIM",
        "CIPLA",
        "IOC",
        "UPL",
        "KOTAKBANK",
        "HDFC",
        "BPCL",
        "BAJAJFINSV",
        "HDFCBANK",
        "INFRATEL",
        "INFY",
        "INDUSINDBK",
        "TCS",
        "POWERGRID",
        "BRITANNIA",
        "ZEEL",
        "SBIN",
        "DRREDDY",
        "NTPC",
        "WIPRO",
        "HEROMOTOCO",
        "YESBANK",
        "HCLTECH",
        "SUNPHARMA",
        "ASIANPAINT",
        "HINDUNILVR",
        "TATAMOTORS",
        "MARUTI",
        "COALINDIA",
        "RELIANCE",
        "ITC",
        "AXISBANK",
        "TITAN",
        "BHARTIARTL",
        "LT",
        "ICICIBANK",
        "GAIL",
        "ONGC",
        "TECHM",
        "IBULHSGFIN",
    ]

    indexes_t = [
        "NIFTY 50",
        "NIFTY 100",
        "NIFTY 200",
        "NIFTY MIDCAP 50",
        "NIFTY MIDCAP 100",
        "INDIA VIX",
    ]
    indexes = ["NIFTY 50"]

    stocks_for_later = ["GRANULES"]

    number_of_buckets = 10
    stock_to_consider_for_trading = 400
    max_trade_amount = 50000
    trading_charges = 0.00101
    overnight_long_charges = 0.0003
    max_order_placement_amount = 50000
    max_single_order_amount = 75000
    candle_data_path = "/tmp/candle_data/"

    base_path = ConstString.base_path

    home = expanduser("~")

    stock_data_path = "{}/stock_data/".format(home)
    stock_temp_data = "{}/stock_temp_data/".format(home)

    logger = LoggerUtils.setup_logger("main_logger", "trading")
    order_execution_logger = LoggerUtils.setup_logger(
        "order_execution", "order_execution"
    )
    historical_data_logger = LoggerUtils.setup_logger(
        "hist_data_looger", "historical_data"
    )
    tick_logger = LoggerUtils.setup_logger("tick_logger", "tick")

    date_format_without_zone = "%Y-%m-%d %H:%M:%S"
    hour_min_format = "%H:%M"
    kite_object_path = "/tmp/kite_object.pickle"

    instance_type = ""
    region = ""
    try:
        region = ec2_metadata.region
        instance_type = ec2_metadata.instance_type
    except Exception as e:
        pass

    @staticmethod
    def move_to_local(data, stock_name, interval, folder_path=None):
        if folder_path == None:
            folder_path = Constants.base_path + "/tmp/stock_data_local/" + interval + "/"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = folder_path + stock_name + ".csv"

        print("saving stock at {}".format(file_path))
        data[stock_name].to_csv(file_path, sep=",", index=False)
        return

    @staticmethod
    def modification_date(filename):
        t = os.path.getmtime(filename)
        return datetime.fromtimestamp(t)

    @staticmethod
    def get_json(data):
        data = json.dumps(data, default=Constants.myconverter)
        data = json.loads(data)
        return data

    @staticmethod
    def myconverter(o):
        if isinstance(o, datetime):
            return o.__str__()
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return float(o)
        if isinstance(o, np.int64):
            return int(o)

    @staticmethod
    def round_to_tick(number):
        return round(number * 20) / 20

    @staticmethod
    def get_india_datetime(d):
        timestamp = int(d.strftime("%s"))
        india_datetime = datetime.fromtimestamp(timestamp, india_tz)
        return india_datetime

    @staticmethod
    def getCurrentMemoryUsage():
        # gives a single float value
        print("CPU percentage {}".format(psutil.cpu_percent()))

        process = psutil.Process(os.getpid())
        mem = process.get_memory_info()[0] / float(2**20)
        print("Memory {}".format(mem))
        # you can convert that object to a dictionary

        return None

    @staticmethod
    def get_future_suffix(index):
        months = [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
        ]

        d = datetime.now()
        month = d.month
        return str(d.year)[-2:] + months[(month + index - 1) % 12] + "FUT"

    @staticmethod
    def get_alphas(day_candle_data, bucket="nifty", suffix="bucket", market_alpha=False):
        alphas = [
            k for k in day_candle_data.columns if "alpha" in k and "market_alpha" not in k
        ]

        if market_alpha == True:
            alphas = [k for k in day_candle_data.columns if "market_alpha" in k]

        if bucket == None:
            raise ("bucket can't be none")

        alphas = [k for k in alphas if bucket in k]
        alphas_copy = []
        for alpha in alphas:
            alphas_copy.append(alpha.split(bucket)[0] + bucket)

        alphas = list(set(alphas_copy))

        return [k + "_" + suffix for k in alphas]

    @staticmethod
    def get_futures_list(stocks, index=None):
        future_suffix = []

        if index == None:
            for i in range(0, 3):
                future_suffix.append(Constants.get_future_suffix(i))
        else:
            if index > 2 or index < 0:
                raise Exception("Invalid index value")
            future_suffix.append(Constants.get_future_suffix(index))

        response = []
        for stock in stocks:
            response.append(stock)

            if stock == "NIFTY 50":
                continue

            for f in future_suffix:
                response.append(stock + f)

        return response


class MarketTime(NamedTuple):
    hour: int
    minute: int

    def ticks_until(
        self, other: "MarketTime", tick_interval: str = TickInterval.five_minute
    ) -> int:
        """Returns number of ticks until the other market time where each tick covers tick_interval
        time. Tick interval defaults to TickInterval.five_minute

        Usage:
        ------
         >>> MarketTime(9,25).ticks_until(MarketTime(13,55))
         54
        """
        end_date = datetime.now().replace(hour=other.hour, minute=other.minute)
        start_date = end_date.replace(hour=self.hour, minute=self.minute)
        date_diff = end_date - start_date
        return int(
            date_diff.total_seconds() // TickInterval.get_interval_seconds(tick_interval)
        )


class SQSConstants:
    screen_snapshot_queue_url = (
        "https://sqs.ap-south-1.amazonaws.com/612481995471/screen_snapshot_queue"
    )


class ZerodhaServiceConstants:
    zerodha = "ZERODHA"
    token = "TOKEN"
    request_token = "request_token"
    kite_oject = "kite_oject"


class DynamoDbConstants:
    dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
    stock_table = dynamodb.Table("StockData")
    orders_table = dynamodb.Table("Orders")
    configuration_table = dynamodb.Table("Configuration")
    machine_task_table = dynamodb.Table("MachineTask")


class StrategyType:
    intraday = "intraday"
    interday = "interday"
    overnight = "overnight"
    overnight_long = "overnight_long"
    overnight_short = "overnight_short"


class ExchangeName:
    nse = "NSE"
    nfo = "NFO"


class StrategySegment:
    index = "index"
    future = "future"
    equity = "equity"


class StrategyBucket:
    future = "future"
    top_500 = "500"


class ExecutionAlgorithm:
    # Transaction type
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"

    limit_order_20s_m = "limit_order_20s_m"
    limit_order_20s = "limit_order_20s"
    limit_order_20s_m2 = "limit_order_20s_m2"

    pike_place_market = "pike_place_market"
    dubrovnik_market = "dubrovnik_market"

    # M3 all modification for short sell orders will happen at buy price (including order placement)
    limit_order_20s_m3 = "limit_order_20s_m3"

    market = "market"


class S3Constants:
    historical_data = "chasing-alpha-historical-data"
    stock_data = "chasing-alpha-stock-data"


class S3Bucket:
    chasing_alpha_market_data = "chasing-alpha-market-data"
    chasing_alpha_ml_models_prod = "chasing-alpha-ml-models-prod"
    chasing_alpha_ml_models_beta = "chasing-alpha-ml-models-beta"


class StockTableColumns:
    AVG_VOL_90 = "AVG_VOL_90"
    Industry = "Industry"
    AVG_VOL_10 = "AVG_VOL_10"
    Last = "Last"
    StockPrice = "StockPrice"
    StockVolume = "StockVolume"
    P_95_5_MINUTE = "P_95_5_MINUTE"
    P_90_5_MINUTE = "P_90_5_MINUTE"
    P_70_5_MINUTE = "P_70_5_MINUTE"
    P_50_5_MINUTE = "P_50_5_MINUTE"
    P_60_5_MINUTE = "P_60_5_MINUTE"
    Volume = "Volume"
    Vwap = "VWAP"
    ZerodhaVwap = "ZerodhaVwap"
    TotalVolume = "TotalVolume"
    VwapPrice = "VwapPrice"
    stock = "stock"


class TickColumns:
    nifty_500_close = "nifty_500_close"
    quantityTraded = "quantityTraded"
    efficiency = "efficiency"


class StockVolume:
    Extreme = "Extreme"
    High = "High"
    Okay = "Okay"


class StockPrice:
    MegaCap = "MegaCap"
    Large = "Large"
    Penny = "Penny"


class DataframeFilters:
    @staticmethod
    def filter(df, apply_strategy=False):
        pass


class OrderType:
    market = "MARKET"
    slm = "SL-M"
    sl = "SL"
    limit = "LIMIT"


class Product:
    bracket = "BO"
    mis = "MIS"
    cnc = "CNC"
    nrml = "NRML"


class OrderVariety:
    bo = "bo"
    regular = "regular"


class PlatformArgs:
    push_trades = "push_trades"
    dump_day_candles = "dump_day_candles"


class Order:
    total_charges = "total_charges"
    stamp_charges = "stamp_charges"
    gst_charges = "gst_charges"
    brokerage_charges = "brokerage_charges"
    combined_exposure = "combined_exposure"
    exchange_transaction_charges = "exchange_transaction_charges"
    actual_tradingsymbol = "actual_tradingsymbol"
    order_type = "order_type"
    tag = "tag"
    disclosed_quantity = "disclosed_quantity"
    child_orders = "child_orders"
    quantity = "quantity"
    pending_quantity = "pending_quantity"
    last_price = "last_price"
    price = "price"
    strategy_price = "strategy_price"
    tradingsymbol = "tradingsymbol"
    exchange = "exchange"
    trade_id = "trade_id"
    product = "product"
    transaction_type = "transaction_type"
    order_timestamp = "order_timestamp"
    average_price = "average_price"
    entry_price = "entry_price"
    sell_side_price = "sell_side_price"
    buy_side_price = "buy_side_price"
    closing_timestamp = "closing_timestamp"
    squareoff = "squareoff"
    is_intraday = "is_intraday"
    stt_charges = "stt_charges"
    trade_amount = "trade_amount"
    trade_number = "trade_number"
    closeQuantity = "closeQuantity"
    close_quantity = "close_quantity"
    sell_transaction = "SELL"
    buy_transaction = "BUY"
    stoploss = "stoploss"
    oms_version = "oms_version"
    place_without_stoploss = "place_without_stoploss"
    pseudo_order_id = "pseudo_order_id"
    pseudo_parent_order_id = "pseudo_parent_order_id"
    close_price = "close_price"
    change = "change"
    seconds_since_midnight = "seconds_since_midnight"
    number_of_tick = "number_of_tick"
    mom = "mom"
    mfi = "mfi"
    traded_amount = "traded_amount"
    macd_width = "macd_width"
    bbwidth = "bbwidth"
    price_wrt_vwap = "price_wrt_vwap"
    rsi = "rsi"
    volatility = "volatility"
    percentage_change = "percentage_change"
    variety = "variety"
    profit = "profit"
    pnl_percentage = "pnl_percentage"
    exposure = "exposure"
    profit_without_transaction = "profit_without_transaction"
    status = "status"
    closed_by = "closed_by"
    buy = "BUY"
    sell = "SELL"
    day_trading_exit = "day_trading_exit"
    parent_order_id = "parent_order_id"
    child_orders = "child_orders"
    order_id = "order_id"
    trigger_price = "trigger_price"
    mode = "mode"
    is_position_closed = "is_position_closed"


class OrderTableColumns:
    order_id = Order.order_id
    execution_time = "execution_time"
    volumePercentile = "volumePercentile"
    order_price = "order_price"
    closed_by = "closed_by"
    balance = "balance"
    closingTimestamp = "closing_timestamp"
    execution_algorithm = "execution_algorithm"
    modification_count = "modification_count"
    child_modification_count = "child_modification_count"
    closeQuantity = "closeQuantity"
    close_price = Order.close_price
    mode = Order.mode
    weighted_intraday_close = "weighted_intraday_close"
    strategy_type = "strategy_type"
    strategy_bucket = "strategy_bucket"
    next_day_intraday_open = "next_day_intraday_open"

    all_columns = [
        Order.order_id,
        Order.order_timestamp,
        Order.closing_timestamp,
        Order.variety,
        Order.tradingsymbol,
        Order.transaction_type,
        Order.quantity,
        Order.profit,
        Order.tag,
        Order.average_price,
        execution_time,
        order_price,
        volumePercentile,
        closed_by,
        Order.entry_price,
        Order.exposure,
        Order.profit_without_transaction,
        balance,
        mode,
        Order.exposure,
        Order.close_price,
        Order.pnl_percentage,
        Order.last_price,
        modification_count,
        execution_algorithm,
        child_modification_count,
        strategy_type,
        strategy_bucket,
        Order.order_type,
        Order.trade_id,
        Order.place_without_stoploss,
        Order.exchange,
        Order.product,
        Order.is_position_closed,
    ]

    portfolio_columns = all_columns + [
        "symbol",
        "stoploss",
        "original_tag",
        weighted_intraday_close,
        next_day_intraday_open,
        "next_date",
    ]


class SlippageMetricsTableColumns:
    order_id = Order.order_id
    entry_slippage = "entry_slippage"
    exit_slippage = "exit_slippage"
    backtest_pnl = "backtest_pnl"
    order_timestamp = "order_timestamp"
    tt = "tt"
    original_pnl = "original_pnl"
    prod_entry_price = "prod_entry_price"
    prod_exit_price = "prod_exit_price"
    backtest_entry_price = "backtest_entry_price"
    backtest_exit_price = "backtest_exit_price"
    prod_exposure = "prod_exposure"
    backtest_exposure = "backtest_exposure"
    prod_pnl = "prod_pnl"
    prod_quantity = "prod_quantity"
    backtest_quantity = "backtest_quantity"

    all_columns = [
        order_id,
        backtest_pnl,
        Order.tag,
        Order.tradingsymbol,
        prod_entry_price,
        prod_exit_price,
        backtest_entry_price,
        backtest_exit_price,
        prod_pnl,
        order_timestamp,
        OrderTableColumns.execution_algorithm,
        prod_exposure,
        backtest_exposure,
        prod_quantity,
        backtest_quantity,
        OrderTableColumns.closingTimestamp,
        "liquidity_bucket_500",
        "liquidity",
        "liquidity_20",
        "is_fno",
    ]


class StrategyMetricsTableColumns:
    a_sharpe_ratio = "a_sharpe_ratio"
    weekly_sharpe_ratio = "weekly_sharpe_ratio"
    monthly_sharpe_ratio = "monthly_sharpe_ratio"
    monthly_pnl = "monthly_pnl"
    exposure_90 = "exposure_90"
    sharpe_ratio = "sharpe_ratio"
    winning_streak = "winning_streak"
    lossing_streak = "lossing_streak"
    avg_profit = "avg_profit"
    avg_loss = "avg_loss"
    max_drawdown = "max_drawdown"
    unique_stocks = "unique_stocks"
    max_drawdown_days = "max_drawdown_days"
    max_gain = "max_gain"
    max_loss = "max_loss"
    tag = "tag"
    trade_amount = "trade_amount"
    year = "year"
    avg_pnl = "avg_pnl"
    success_ratio = "success_ratio"
    bps = "bps"
    slippage = "slippage"
    total_signals = "total_signals"
    number_of_losses = "number_of_losses"
    number_of_wins = "number_of_wins"
    all_columns = [
        avg_pnl,
        success_ratio,
        total_signals,
        number_of_losses,
        number_of_wins,
        a_sharpe_ratio,
        sharpe_ratio,
        winning_streak,
        lossing_streak,
        avg_profit,
        avg_loss,
        max_drawdown,
        max_gain,
        max_loss,
        tag,
        year,
        weekly_sharpe_ratio,
        trade_amount,
        monthly_sharpe_ratio,
        bps,
        slippage,
        monthly_pnl,
        exposure_90,
        max_drawdown_days,
        unique_stocks,
    ]


class StrategyTags:
    vyakul = "vyakul"
    roger = "roger"
    messi = "messi"
    ronaldo = "ronaldo"
    main = "main"
    suarez = "suarez"
    amazon = "amazon"
    arham = "arham"
    bruce = "bruce"
    harvey = "harvey"
    jessica = "jessica"
    mario = "mario"
    kipchoge = "kipchoge"
    sam = "sam"
    ellen = "ellen"
    root = "root"
    murdock = "murdock"
    winry = "winry"
    jack = "jack"
    zlatan = "zlatan"
    shifu = "shifu"
    batman = "batman"
    djokovic = "djokovic"
    nadal = "nadal"
    python = "python"
    panda = "panda"
    kenmiles = "kenmiles"
    morningreversion = "morningreversion"


class Strategies:
    TestStrategy = "TestStrategy"
    Midday = "Midday"
    KenmilesN = "KenmilesN"
    Suarez = "Suarez"
    VyakulN = "VyakulN"
    Witcher = "Witcher"
    Jack = "Jack"
    Root = "Root"
    Finch = "Finch"
    Queen = "Queen"
    Harvey = "Harvey"
    Terstegen = "Terstegen"
    PortfolioN = "PortfolioN"
    MustangN = "MustangN"
    Stark = "Stark"
    Roach = "Roach"
    Musk = "Musk"
    Ellen = "Ellen"
    Trevor = "Trevor"
    Keanu = "Keanu"
    MorningReversion = "MorningReversion"
    House = "House"
    Roger = "Roger"
    Nadal = "Nadal"
    Matsya = "Matsya"
    Bruno = "Bruno"
    Cartman = "Cartman"
    Fnoshort = "Fnoshort"
    fno_port = "fno_port"
    terstegen_fno = "terstegen_fno"
    harvey_fno = "harvey_fno"


class OrderStatus:
    complete = "COMPLETE"
    cancelled = "CANCELLED"
    open = "OPEN"
    rejected = "REJECTED"
    trigger_pending = "TRIGGER PENDING"
    modify_validation_pending = "MODIFY VALIDATION PENDING"
    validation_pending = "VALIDATION PENDING"


class StrategyConfigs:
    strategy_config_path = "/quantplay/strategies/strategy_configs"
    base_path = Constants.base_path + strategy_config_path
    profiler = base_path + "/profiler.json"
    prod = base_path + "/prod.json"
    pre_prod = base_path + "/pre_prod.json"
    backtest_set1 = base_path + "/backtest_set1.json"


class TradingMode:
    replayTick = "replayTick"
    prod = "prod"
    backtest = "backtest"
    profiler = "profiler"
    prod_verfication = "prod_verification"
    optimize = "optimize"


class FeedName:
    S3 = "s3"


class MLModels:
    matsya_beta = "/tmp/matsya.sav"


class TradingCode:
    ok = "200"
    exit_all = "400"


def timeit(*args_main, **kwargs_main):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            ts = time.time()
            result = function(*args, **kwargs)
            te = time.time()
            if "MetricName" in kwargs_main:
                data = {
                    "MetricName": kwargs_main["MetricName"],
                    "Unit": "Seconds",
                    "Value": (te - ts),
                    "Dimensions": [
                        {"Name": "Region", "Value": Constants.region},
                        {
                            "Name": "InstanceType",
                            "Value": Constants.instance_type,
                        },
                    ],
                }
                Constants.logger.info("{}".format(json.dumps(data)))
            else:
                Constants.logger.error("No metric found in {}".format(function.__name__))
            return result

        return wrapper

    return inner_function
