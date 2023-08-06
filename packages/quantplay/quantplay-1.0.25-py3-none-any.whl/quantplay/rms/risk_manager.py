from quantplay_utils.wrapper.mysql_wrapper import StrategyMetricsTable
import pandas as pd

class RiskManager:
    @staticmethod
    def check_risk_of_new_strategy(response=None):
        with StrategyMetricsTable() as table:
            strategy_metrics = table.fetch_data()
        strategy_metrics = pd.DataFrame(strategy_metrics)
        strategy_metrics = strategy_metrics[strategy_metrics.year == "ALL"]
        
        median_bps = strategy_metrics.bps.quantile(.5)
        median_max_drawdown = strategy_metrics.max_drawdown.quantile(.5)
        median_sharpe_ratio = strategy_metrics.sharpe_ratio.quantile(.5)
        median_weekly_sharpe_ratio = strategy_metrics.weekly_sharpe_ratio.quantile(.5)
        median_total_signals = strategy_metrics.total_signals.quantile(.5)
        median_unique_stocks = strategy_metrics.unique_stocks.quantile(.5)
        median_max_drawdown_days = strategy_metrics.max_drawdown_days.quantile(.5)
        median_monthly_pnl = strategy_metrics.monthly_pnl.quantile(.5)
        median_exposure_90 = strategy_metrics.exposure_90.quantile(.5)
        
        if not response:
            print("Median bps {} ".format(median_bps))
            print("Median max_drawdown {}".format(median_max_drawdown))
            print("Median sharpe_ratio {}".format(median_sharpe_ratio))
            print("Median weekly_sharpe_ratio {}".format(median_weekly_sharpe_ratio))
            print("Median total_signals {}".format(median_total_signals))
            print("Median unique_stocks {}".format(median_unique_stocks))
            print("Median max_drawdown_days {}".format(median_max_drawdown_days))
            print("Median monthly_pnl {}".format(median_monthly_pnl))
            print("Median exposure_90 {}".format(median_exposure_90))
        else:
            overall_results = list(filter(lambda x: x['year'] == 'ALL', response))[0]
            
        