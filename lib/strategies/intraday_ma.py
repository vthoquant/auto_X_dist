# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:40:09 2021

@author: vivin
"""
from lib.strategies.base_classes import INTRADAY_BASE
from lib.configs.directory_names import STRATEGY_RUN_BASE_PATHS
import pandas as pd
import numpy as np
import datetime
from talib.abstract import EMA, ROCP, MACD, ATR

class INTRADAY_MA(INTRADAY_BASE):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_MA']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, ema_window=None, on_heikin_ashi=None, eod_sqoff=True, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = INTRADAY_MA.TRADE_STATES.Start
        self.ema_window = ema_window
        self.on_heikin_ashi = on_heikin_ashi or False
        self.eod_sqoff = eod_sqoff
        self.min_bars_to_trade = 2
        self._state_vars = {'entry_state': None, 'entry_rsi': None, 'entry_signal': None, 'entry_macd': None, 'entry_rocp': None, 'entry_price': None, 'prev_state': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        #data = self.extended_mkt.loc[dt]
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self.indicators_to_publish['EMA'] = data['EMA']
        self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
        self._state_vars['prev_state'] = self.trade_state
        if self.run_bars_since_sod >= self.min_bars_to_trade:            
            #update per asset capital based on c-c returns
            if self.units_whole[ticker] >= 0:
                #if long then per_asset_capital increase is directly proportional to returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+self.inst_delta*returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            else:
                #if short then per asset capital increase is inversely proportional to returns
                self.per_asset_capital[ticker] = max(self.per_asset_capital[ticker] * (1-self.inst_delta*returns), 0.0) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            is_trade_bar = self._generate_trades_on_indicators(data, dt, data['isEOD'])
        else:
            self.indicators_to_publish['Signal'] = None
            self.indicators_to_publish['trade_state'] = self.trade_state
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        ema = data['EMA'] if not self.on_heikin_ashi else data['EMA_HA']
        price_close = data['{} Close'.format(ticker)] if not self.on_heikin_ashi else data['Close_HA']
        buy_signal = price_close > ema
        sell_signal = price_close < ema
        
        if not isEOD or not self.eod_sqoff:
            if self.trade_state == INTRADAY_MA.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
                elif sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_buy:
                if sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_sell:
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = INTRADAY_MA.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar
        
    def prepare_strategy_attributes(self, dt=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        day_in_pydt = pd.Series(np.vectorize(lambda x: x.day)(pd.Series(self.extended_mkt.index.values).map(datetime.datetime.date)))
        self.extended_mkt['isEOD'] = (day_in_pydt != day_in_pydt.shift(-1)).values
        if dt is not None:
            #hack for live run
            self.extended_mkt.loc[dt, 'isEOD'] = False
        ticker = self.tickers[0]
        
        self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
        if self.on_heikin_ashi:
            self._extend_attrs_for_ha(dt)
        self.extended_mkt['EMA'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.ema_window) 
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _extend_attrs_for_ha(self, dt=None):
        ticker = self.tickers[0]
        self.extended_mkt = self.extended_mkt.loc[:dt].iloc[-5:] if dt is not None else self.extended_mkt
        o, h, l, c = ['{} {}'.format(ticker, x) for x in ['Open', 'High', 'Low', 'Close']]
        ha_open_l, ha_high_l, ha_low_l, ha_close_l, ha_barlen_l = [self.extended_mkt.iloc[0][o]], [self.extended_mkt.iloc[0][h]], [self.extended_mkt.iloc[0][l]], [self.extended_mkt.iloc[0][c]], [self.extended_mkt.iloc[0][c] - self.extended_mkt.iloc[0][o]]
        
        prices_open = self.extended_mkt[o].values
        prices_high = self.extended_mkt[h].values
        prices_low = self.extended_mkt[l].values
        prices_close = self.extended_mkt[c].values
        for index in range(0, len(self.extended_mkt)):
            if index == 0:
                continue
            prev_ha_open = ha_open_l[index-1]
            prev_ha_close = ha_close_l[index-1]
            curr_ha_close = (prices_open[index] + prices_high[index] + prices_low[index] + prices_close[index]) * 0.25
            curr_ha_open = (prev_ha_open + prev_ha_close) * 0.5
            ha_barlen_l.append(curr_ha_close - curr_ha_open)
            ha_close_l.append(curr_ha_close)
            ha_open_l.append(curr_ha_open)
            ha_high_l.append(max(prices_high[index], curr_ha_close, curr_ha_open))
            ha_low_l.append(min(prices_low[index], curr_ha_close, curr_ha_open))
        
        ha_dict = dict(zip(['Open_HA', 'High_HA', 'Low_HA', 'Close_HA', 'HA_barlen'], [ha_open_l, ha_high_l, ha_low_l, ha_close_l, ha_barlen_l])) 
        ha_ext = pd.DataFrame(data=ha_dict, index=self.extended_mkt.index.values)
        self.extended_mkt = pd.concat([self.extended_mkt, ha_ext], axis=1)
        self.extended_mkt['EMA_HA'] = EMA(self.extended_mkt['Close_HA'], timeperiod=self.ema_window)
                
class INTRADAY_MAC(INTRADAY_MA):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_MAC']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, ema_window_short=None, ema_long_window_mult=None, mean_rev=False, wait_for_crossover=True, restrict_trade_time=True, no_trade_days=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = INTRADAY_MA.TRADE_STATES.Start
        self.ema_window_short = ema_window_short
        self.ema_window_long = int(ema_window_short * ema_long_window_mult)
        self.mean_rev = mean_rev
        self.wait_for_crossover = wait_for_crossover
        self.restrict_trade_time = restrict_trade_time
        self.no_trade_days = no_trade_days or (5,)
        self.min_bars_to_trade = 2
        self._state_vars = {'prev_state': None, 'entry_signal': None, 'entry_day': None, 'entry_hour': None, 'sod_signal': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self.indicators_to_publish['EMA_short'] = data['EMA_short']
        self.indicators_to_publish['EMA_long'] = data['EMA_long']
        self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
        self._state_vars['prev_state'] = self.trade_state
        if self.run_bars_since_sod >= self.min_bars_to_trade and ~np.isnan(self.indicators_to_publish['EMA_long']):            
            #update per asset capital based on c-c returns
            if self.units_whole[ticker] >= 0:
                #if long then per_asset_capital increase is directly proportional to returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+self.inst_delta*returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            else:
                #if short then per asset capital increase is inversely proportional to returns
                self.per_asset_capital[ticker] = max(self.per_asset_capital[ticker] * (1-self.inst_delta*returns), 0.0) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            is_trade_bar = self._generate_trades_on_indicators(data, dt, data['isEOD'])
        else:
            self.indicators_to_publish['Signal'] = None
            self.indicators_to_publish['trade_state'] = self.trade_state
            self._update_statevar_based_indicators(isnone=True)
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        ema_long = self.indicators_to_publish['EMA_long']
        ema_short = self.indicators_to_publish['EMA_short']
        buy_signal = ema_short > ema_long if not self.mean_rev else ema_short < ema_long
        sell_signal = ema_short < ema_long if not self.mean_rev else ema_short > ema_long
        
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        
        if not isEOD:
            if self.trade_state == INTRADAY_MA.TRADE_STATES.Intraday_squareoff:
                if self._state_vars['sod_signal'] is None:
                    self._state_vars['sod_signal'] = 'BUY' if buy_signal else 'SELL'
                    
                if buy_signal and not no_trade and (self._state_vars['sod_signal'] == 'SELL' or not self.wait_for_crossover): #only trade at sod once crossover happens
                    self._update_statevar_based_indicators()
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
                    self._update_statevars(dt, signal)
                    self._state_vars['sod_signal'] = 'COMPLETE'
                elif sell_signal and not no_trade and (self._state_vars['sod_signal'] == 'BUY' or not self.wait_for_crossover): #only trade at sod once crossover happens
                    self._update_statevar_based_indicators()
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
                    self._update_statevars(dt, signal)
                    self._state_vars['sod_signal'] = 'COMPLETE'
                else:
                    self._update_statevar_based_indicators(isnone=True)
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_buy:
                if sell_signal and not no_trade:
                    self._update_statevar_based_indicators()
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
                    self._update_statevars(dt, signal)
                elif sell_signal and no_trade:
                    #this will only happen during an existing trading day when we go past the cutoff time
                    self._update_statevar_based_indicators()
                    signal = 0
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff
                    self._update_statevars(dt, signal)
                else:
                    self._update_statevar_based_indicators(isnone=True)
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_sell:
                if buy_signal and not no_trade:
                    self._update_statevar_based_indicators()
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
                    self._update_statevars(dt, signal)
                elif buy_signal and not no_trade:
                    #this will only happen during an existing trading day when we go past the cutoff time
                    self._update_statevar_based_indicators()
                    signal = 0
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff
                    self._update_statevars(dt, signal)
                else:
                    self._update_statevar_based_indicators(isnone=True)
            else:
                self._update_statevar_based_indicators(isnone=True)
                signal = None
                if not no_trade:
                    print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        elif isEOD and self.trade_state != INTRADAY_MA.TRADE_STATES.Intraday_squareoff:
            self._update_statevar_based_indicators()
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = INTRADAY_MA.TRADE_STATES.Start #reset this attribute for next days run
            self._update_statevars(dt, signal)
        elif isEOD:
            self._state_vars['sod_signal'] = None #reset the sod state
        else:
            self._update_statevar_based_indicators(isnone=True)
            signal = None
            if not no_trade:
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar
        
    def prepare_strategy_attributes(self, dt=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        day_in_pydt = pd.Series(np.vectorize(lambda x: x.day)(pd.Series(self.extended_mkt.index.values).map(datetime.datetime.date)))
        self.extended_mkt['isEOD'] = (day_in_pydt != day_in_pydt.shift(-1)).values
        if dt is not None:
            #hack for live run
            self.extended_mkt.loc[dt, 'isEOD'] = False
        ticker = self.tickers[0]
        
        self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
        self.extended_mkt['EMA_long'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.ema_window_long)
        self.extended_mkt['EMA_short'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.ema_window_short)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _update_statevars(self, dt, signal):
        py_dt = pd.Timestamp(dt).to_pydatetime()
        self._state_vars['entry_day'] = py_dt.weekday()
        '''
        if py_dt.hour < 11:
            self._state_vars['entry_hour'] = 1
        elif py_dt.hour < 14:
            self._state_vars['entry_hour'] = 2
        else:
            self._state_vars['entry_hour'] = 3
        '''
        self._state_vars['entry_hour'] = py_dt.hour
        self._state_vars['entry_signal'] = signal
        
    def _update_statevar_based_indicators(self, isnone=False):
        self.indicators_to_publish['entry_day'] = self._state_vars['entry_day'] if not isnone else None
        self.indicators_to_publish['entry_hour'] = self._state_vars['entry_hour'] if not isnone else None
        self.indicators_to_publish['entry_signal'] = self._state_vars['entry_signal'] if not isnone else None
        
    def _no_trade_condition(self, dt):
        py_dt = pd.Timestamp(dt).to_pydatetime()
        if py_dt.hour < 10 or py_dt.hour > 14:
            return True
        if py_dt.weekday() in self.no_trade_days:
            return True
        
        return False
        
class INTRADAY_MACD(INTRADAY_MA):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_MACD']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, window_short=None, long_window_mult=None, signal_window_mult=None, restrict_trade_time=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = INTRADAY_MA.TRADE_STATES.Start
        self.window_short = window_short
        self.window_long = int(window_short * long_window_mult)
        self.window_signal = int(window_short * signal_window_mult)
        self.min_bars_to_trade = 2
        self.restrict_trade_time = restrict_trade_time or False
        self._state_vars = {'prev_state': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self.indicators_to_publish['MACD_hist'] = data['MACD_hist']
        self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
        self._state_vars['prev_state'] = self.trade_state
        if self.run_bars_since_sod >= self.min_bars_to_trade and ~np.isnan(self.indicators_to_publish['MACD_hist']):            
            #update per asset capital based on c-c returns
            if self.units_whole[ticker] >= 0:
                #if long then per_asset_capital increase is directly proportional to returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+self.inst_delta*returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            else:
                #if short then per asset capital increase is inversely proportional to returns
                self.per_asset_capital[ticker] = max(self.per_asset_capital[ticker] * (1-self.inst_delta*returns), 0.0) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            is_trade_bar = self._generate_trades_on_indicators(data, dt, data['isEOD'])
        else:
            self.indicators_to_publish['Signal'] = None
            self.indicators_to_publish['trade_state'] = self.trade_state
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        signal = None
        buy_signal = self.indicators_to_publish['MACD_hist'] > 0
        sell_signal = self.indicators_to_publish['MACD_hist'] < 0
        
        if not isEOD:
            if self.trade_state == INTRADAY_MA.TRADE_STATES.Intraday_squareoff:
                if buy_signal and not no_trade:
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
                elif sell_signal and not no_trade:
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_buy:
                if sell_signal and not no_trade:
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
                elif sell_signal and no_trade:
                    signal = 0
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_sell:
                if buy_signal and not no_trade:
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
                elif buy_signal and no_trade:
                    signal = 0
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = INTRADAY_MA.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar
        
    def prepare_strategy_attributes(self, dt=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        day_in_pydt = pd.Series(np.vectorize(lambda x: x.day)(pd.Series(self.extended_mkt.index.values).map(datetime.datetime.date)))
        self.extended_mkt['isEOD'] = (day_in_pydt != day_in_pydt.shift(-1)).values
        if dt is not None:
            #hack for live run
            self.extended_mkt.loc[dt, 'isEOD'] = False
        ticker = self.tickers[0]
        
        self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
        self.extended_mkt['MACD_hist'] = MACD(self.extended_mkt['{} Close'.format(ticker)], fastperiod=self.window_short, slowperiod=self.window_long, signalperiod=self.window_signal)[2]
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _no_trade_condition(self, dt):
        py_dt = pd.Timestamp(dt).to_pydatetime()
        if py_dt.hour < 10 or py_dt.hour > 14:
            return True
        
        return False

class INTRADAY_MAC_SL(INTRADAY_MAC):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_MAC_SL']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, ema_window_short=None, ema_long_window_mult=None, rescale_shorts=False, stop_loss=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super().__init__(identifier, initial_capital, run_bars_since_sod, tickers, ema_window_short, ema_long_window_mult, rescale_shorts, add_transaction_costs, inst_delta, app)
        self.stop_loss = stop_loss
        
    def update_indicators(self, dt=None):
        #data = self.extended_mkt.loc[dt]
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        self.indicators_to_publish['ATR'] = data['ATR']
        super().update_indicators(dt)
    
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        ema_long = self.indicators_to_publish['EMA_long']
        ema_short = self.indicators_to_publish['EMA_short']
        stop_loss_amnt = self.indicators_to_publish['ATR'] * self.stop_loss if self.stop_loss is not None else -999
        stop_long_loss = ema_long - data['{} Close'.format(ticker)] > stop_loss_amnt if self.stop_loss is not None else False
        stop_short_loss = data['{} Close'.format(ticker)] - ema_long > stop_loss_amnt if self.stop_loss is not None else False
        buy_signal = ema_short > ema_long and not stop_long_loss and data['{} Close'.format(ticker)] > ema_long
        sell_signal = ema_short < ema_long and not stop_short_loss and data['{} Close'.format(ticker)] < ema_long
        
        if not isEOD:
            if self.trade_state == INTRADAY_MA.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
                elif sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_buy:
                if stop_long_loss:
                    signal = 0
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff
                elif sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_sell:
                if stop_short_loss:
                    signal = 0
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = INTRADAY_MA.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar
        
    def prepare_strategy_attributes(self, dt=None):
        super().prepare_strategy_attributes(dt)
        self.extended_mkt['ATR'] = ATR(self.extended_mkt['{} High'.format(self.tickers[0])], self.extended_mkt['{} Low'.format(self.tickers[0])], self.extended_mkt['{} Close'.format(self.tickers[0])])
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_MAC_MA(INTRADAY_MAC):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_MAC_MA']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, ema_window_cutoff=None, ema_window_short=None, ema_long_window_mult=None, rescale_shorts=False, stop_loss=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super().__init__(identifier, initial_capital, run_bars_since_sod, tickers, ema_window_short, ema_long_window_mult, None, None, None, None, rescale_shorts, add_transaction_costs, inst_delta, app)
        self.ema_window_cutoff = ema_window_cutoff
        
    def update_indicators(self, dt=None):
        #data = self.extended_mkt.loc[dt]
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        self.indicators_to_publish['EMA_cutoff'] = data['EMA_cutoff']
        super().update_indicators(dt)
    
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        price_close = data['{} Close'.format(ticker)]
        ema_long = self.indicators_to_publish['EMA_long']
        ema_short = self.indicators_to_publish['EMA_short']
        ema_cutoff = self.indicators_to_publish['EMA_cutoff']
        buy_signal = price_close > ema_cutoff and ema_cutoff > ema_short and ema_short > ema_long
        sell_signal = price_close < ema_cutoff and ema_cutoff < ema_short and ema_short < ema_long
        buy_squareoff = price_close <= ema_cutoff
        sell_squareoff = price_close >= ema_cutoff
        
        if not isEOD:
            if self.trade_state == INTRADAY_MA.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
                elif sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_buy:
                if buy_squareoff:
                    signal = 0
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff
                elif sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_MA.TRADE_STATES.Regular_sell:
                if sell_squareoff:
                    signal = 0
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_MA.TRADE_STATES.Regular_buy
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = INTRADAY_MA.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar
        
    def prepare_strategy_attributes(self, dt=None):
        super().prepare_strategy_attributes(dt)
        self.extended_mkt['EMA_cutoff'] = EMA(self.extended_mkt['{} Close'.format(self.tickers[0])], timeperiod=self.ema_window_cutoff)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_MACD_TP_SL(INTRADAY_MACD):    
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_MACD_TP_SL']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, window_short=None, long_window_mult=None, signal_window_mult=None, sl_atr=None, tp_atr=None, watch_reversal=None, is_trailing_sl=None, restrict_trade_time=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_MACD_TP_SL, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, window_short, long_window_mult, signal_window_mult, restrict_trade_time, rescale_shorts, add_transaction_costs, inst_delta, app)
        self._state_vars = {'prev_state': None, 'entry_price': None, 'trailing_price': None}
        #self.sl_perc = sl_perc
        #self.tp_perc = tp_perc
        self.sl_atr = sl_atr
        self.tp_atr = tp_atr
        self.watch_reversal = watch_reversal or False
        self.is_trailing_sl = is_trailing_sl or False
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        price_close = data['{} Close'.format(ticker)]
        atr = data['ATR']
        price_entry = self._state_vars['entry_price']
        price_trailing = self._state_vars['trailing_price']
        signal = None
        buy_signal = self.indicators_to_publish['MACD_hist'] > 0 and self.indicators_to_publish['MACD_hist_prev'] <= 0 and not no_trade
        sell_signal = self.indicators_to_publish['MACD_hist'] < 0 and self.indicators_to_publish['MACD_hist_prev'] >= 0 and not no_trade
        sl_hit_price = price_entry if not self.is_trailing_sl else price_trailing
        buy_squareoff = price_entry is not None and ((price_close - price_entry > atr * self.tp_atr) or (price_close - sl_hit_price < -atr * self.sl_atr))
        sell_squareoff = price_entry is not None and ((price_close - price_entry < -atr * self.tp_atr) or (price_close - sl_hit_price > atr * self.sl_atr))
        
        if not isEOD:
            if self.trade_state == self.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
                elif sell_signal:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
            elif self.trade_state == self.TRADE_STATES.Regular_buy:
                if sell_signal and self.watch_reversal:
                    #do this. macd may reverse sign before tp or sl is hit!
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
                elif buy_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
                    self.indicators_to_publish['trailing_price'] = self._state_vars['trailing_price']
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
                    self._state_vars['trailing_price'] = max(self._state_vars['trailing_price'], price_close)
            elif self.trade_state == self.TRADE_STATES.Regular_sell:
                if buy_signal and self.watch_reversal:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
                elif sell_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
                    self.indicators_to_publish['trailing_price'] = self._state_vars['trailing_price']
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
                    self._state_vars['trailing_price'] = min(self._state_vars['trailing_price'], price_close)
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = self.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar
    
    def prepare_strategy_attributes(self, dt=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        day_in_pydt = pd.Series(np.vectorize(lambda x: x.day)(pd.Series(self.extended_mkt.index.values).map(datetime.datetime.date)))
        self.extended_mkt['isEOD'] = (day_in_pydt != day_in_pydt.shift(-1)).values
        if dt is not None:
            #hack for live run
            self.extended_mkt.loc[dt, 'isEOD'] = False
        ticker = self.tickers[0]
        
        self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
        self.extended_mkt['MACD_hist'] = MACD(self.extended_mkt['{} Close'.format(ticker)], fastperiod=self.window_short, slowperiod=self.window_long, signalperiod=self.window_signal)[2]
        self.extended_mkt['MACD_hist_prev'] = self.extended_mkt['MACD_hist'].shift(1)
        self.extended_mkt['ATR'] = ATR(self.extended_mkt['{} High'.format(ticker)], self.extended_mkt['{} Low'.format(ticker)], self.extended_mkt['{} Close'.format(ticker)])
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self.indicators_to_publish['MACD_hist'] = data['MACD_hist']
        self.indicators_to_publish['MACD_hist_prev'] = data['MACD_hist_prev']
        self.indicators_to_publish['ATR'] = data['ATR']
        self.indicators_to_publish['entry_price'] = None
        self.indicators_to_publish['trailing_price'] = None
        self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
        self._state_vars['prev_state'] = self.trade_state
        if self.run_bars_since_sod >= self.min_bars_to_trade and ~np.isnan(self.indicators_to_publish['MACD_hist']):            
            #update per asset capital based on c-c returns
            if self.units_whole[ticker] >= 0:
                #if long then per_asset_capital increase is directly proportional to returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+self.inst_delta*returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            else:
                #if short then per asset capital increase is inversely proportional to returns
                self.per_asset_capital[ticker] = max(self.per_asset_capital[ticker] * (1-self.inst_delta*returns), 0.0) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            is_trade_bar = self._generate_trades_on_indicators(data, dt, data['isEOD'])
        else:
            self.indicators_to_publish['Signal'] = None
            self.indicators_to_publish['trade_state'] = self.trade_state
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)
    