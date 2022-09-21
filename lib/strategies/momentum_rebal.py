# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 18:23:44 2020

@author: vivin
"""

from lib.engines.strategy_base import STRATEGY_BASE
from lib.configs.directory_names import STRATEGY_RUN_BASE_PATHS
from talib.abstract import ROCP
import pandas as pd
import numpy as np

class MOMENTUM_REBAL_STRATEGY(STRATEGY_BASE):
    db_loc = STRATEGY_RUN_BASE_PATHS['MOMENTUM_REBAL_STRATEGY']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
    def __init__(self, identifier, initial_capital=1000000, run_days=0, tickers=None, ma_window=None, M_c=None, rebal_freq_days=7):
        STRATEGY_BASE.__init__(self, identifier, initial_capital, run_days)
        self.ma_window = ma_window
        self.M_c = M_c
        self.tickers = tickers
        self.days_since_start = 0
        self.weights = dict(zip(tickers, [0.0] * len(tickers)))
        self.weights['Cash'] = 1.0
        self.per_asset_capital = dict(zip(tickers, [0.0] * len(tickers)))
        self.per_asset_capital['Cash'] = initial_capital
        self.rebal_freq_days = rebal_freq_days
        self.live_prices = dict(zip(tickers, [None] * len(tickers)))
        self.units_float = dict(zip(tickers, [0.0] * len(tickers)))
        self.units_whole = self.units_float
        self.units_whole_prev = self.units_whole
        self.per_asset_signal = dict(zip(tickers, [0.0] * len(tickers)))
        self.last_processed_time = None
        
        cols_ohlcv = []
        for value_type in ['Open', 'High', 'Low', 'Close', 'Volume']:
            cols_ohlcv = cols_ohlcv + ['{} {}'.format(x, value_type) for x in self.tickers]
        self.db_cache_mkt = pd.DataFrame(columns=cols_ohlcv + ['TimeStamp']).set_index('TimeStamp')
        position_cols = ['{} Position'.format(x) for x in self.tickers]
        capital_cols = ['{} capital'.format(x) for x in self.tickers + ['Cash']]
        self.db_cache_algo = pd.DataFrame(columns=['TimeStamp'] + cols_ohlcv + capital_cols + position_cols + ['Eq Curve Unrealized', 'Eq Curve Realized']).set_index('TimeStamp')
       
    def generate_signal(self):
        for ticker in self.tickers:
            self.per_asset_signal[ticker] = self.units_whole[ticker] - self.units_whole_prev[ticker]

    def update_indicators(self, dt=None):
        self.run_days = self.run_days + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_day = False
        if self.run_days > self.ma_window:
            self.days_since_start = self.days_since_start + 1
            data = self.extended_mkt.loc[dt]
            mom_dict = {}
            for ticker in self.tickers:
                price = data['{} Close'.format(ticker)]
                returns = data['{} returns'.format(ticker)]
                momentum = data['{} mom'.format(ticker)]
                mom_dict[ticker] = momentum if ~np.isnan(momentum) else -100.0
                self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
                if self.run_days > self.ma_window + 1:
                    #update per asset capital based on c-c returns
                    self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            if self.days_since_start > 1:
                self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            if ((self.days_since_start-1) % self.rebal_freq_days) == 0:
                #rebalance
                is_trade_day = True
                self._rebalance(mom_dict)
        else:
            data = self.extended_mkt.loc[dt]
            for ticker in self.tickers:
                price = data['{} Close'.format(ticker)]
                self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_day)
        
    def prepare_strategy_attributes(self, dt_till=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        for ticker in self.tickers:
            self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
            self.extended_mkt['{} mom'.format(ticker)] = self.extended_mkt['{} returns'.format(ticker)].rolling(self.ma_window).mean()
    
    def _rebalance(self, mom_dict):
        pos_mom_sum = np.array([max(m,0) for m in mom_dict.values()]).sum() + self.M_c
        for ticker, momentum in mom_dict.items():
            self.weights[ticker] = max(momentum,0)/pos_mom_sum if pos_mom_sum != 0.0 else 0.0

        self._allocate_capital_by_weights()
        
    def skip_event(self, events_df):
        skip = False
        skip = skip or (len(events_df) != len(self.tickers))
        return skip
        
    def place_orders(self):
        '''
        for ticker, units in self.per_asset_signal.items():
            print("{}: placing order for {} units of {}".format(self.last_processed_time, units, ticker))
            print("{}: current position in {} is {} units".format(self.last_processed_time, ticker, self.units_whole[ticker]))
        print("{}: current capital is {}".format(self.last_processed_time, self.current_capital))
        '''
        pass

    def square_off(self, dt=None):
        self.units_whole_prev = self.units_whole.copy()
        for ticker in self.tickers:
            self.units_whole[ticker] = 0
            self.per_asset_signal[ticker] = - self.units_whole_prev[ticker]
            self.per_asset_capital[ticker] = 0.0
        self.per_asset_capital['Cash'] = self.current_capital
        self.place_orders()
        self._update_quick_bt_attrs(dt, is_square_off=True)
        
    def compute_perf_metrics(self):
        """
        given all the trade returns, compute typical metrics such as hit ratio, normalized hit ratio etc
        """
        trade_returns = self.db_cache_algo['Eq Curve Realized'].dropna().pct_change().dropna()
        metrics = self.compute_perf_metrics_base(trade_returns, self.days_since_start)
        return(metrics)
        
    
