from quantplay.utils.constant import TradingCode


class StrategyResponse:
    def __init__(self):
        self.new_orders = {}
        self.trades_to_close = {}
        self.response_code = TradingCode.ok
