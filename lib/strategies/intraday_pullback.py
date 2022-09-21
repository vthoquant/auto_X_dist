# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 19:03:25 2021

@author: vivin
"""
from lib.strategies.base_classes import INTRADAY_BASE
from lib.configs.directory_names import STRATEGY_RUN_BASE_PATHS
from talib.abstract import ROCP, RSI, EMA, BBANDS
from talib.abstract import CDLHAMMER, CDLSHOOTINGSTAR, CDLGRAVESTONEDOJI, CDLDRAGONFLYDOJI, CDLINVERTEDHAMMER, CDLHANGINGMAN, CDLMORNINGDOJISTAR, CDLMORNINGSTAR, CDLEVENINGDOJISTAR, CDLEVENINGSTAR, CDLENGULFING, CDLHARAMI 
import numpy as np
import pandas as pd
import datetime

class INTRADAY_PULLBACK(INTRADAY_BASE):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_PULLBACK']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, rsi_period=None, rsi_entry=None, rsi_exit=None, max_holding=None, trend_baseline=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Start
        self.rsi_period = rsi_period
        self.rsi_entry = rsi_entry or (5, 95)
        self.rsi_exit = rsi_exit or (55, 45)
        self.max_holding = max_holding or 5
        self.trend_baseline = trend_baseline or 20
        self.side_restriction = side_restriction
        self.min_bars_to_trade = 2   #hardcoded for now
        self.bars_since_trade = None
        self.restrict_trade_time = restrict_trade_time or False
        self._state_vars = {'entry_state': None, 'entry_rsi': None, 'entry_ema': None, 'entry_signal': None, 'entry_price': None, 'bars_since_trade': None, 'prev_state': None}
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
        self._update_indicators_to_publish(data)
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
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['EMA'] = data['EMA']
        self.indicators_to_publish['RSI'] = data['RSI']
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff = self._generate_trade_conditions(data, dt)
        is_trade_bar = self._process_conditions(data, dt, signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff, isEOD)
        return is_trade_bar
    
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_PULLBACK.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        signal = None
        ema = data['EMA']
        rsi = data['RSI']
        buy_signal = data['{} Close'.format(ticker)] > ema and rsi < self.rsi_entry[0] and not no_trade
        buy_squareoff = rsi > self.rsi_exit[0] or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        sell_signal = data['{} Close'.format(ticker)] < ema and rsi > self.rsi_entry[1] and not no_trade
        sell_squareoff = rsi < self.rsi_exit[1] or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
    
    def _process_conditions(self, data, dt, signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff, isEOD=False):
        if hasattr(self, 'side_restriction'):
            if self.side_restriction == 1:
                #only long trades allowed
                sell_signal, sell_squareoff = False, False
            elif self.side_restriction == -1:
                #only short trades allowed
                buy_signal, buy_squareoff = False, False

        ticker = self.tickers[0]
        price_close = data['{} Close'.format(ticker)]
        if not isEOD:
            if self.trade_state == self.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                elif sell_signal:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
            elif self.trade_state == self.TRADE_STATES.Regular_buy:
                if buy_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self._state_vars['entry_price'] = None
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
            elif self.trade_state == self.TRADE_STATES.Regular_sell:
                if sell_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self._state_vars['entry_price'] = None
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
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
        self.extended_mkt['EMA'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.trend_baseline)
        self.extended_mkt['RSI'] = RSI(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.rsi_period)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _no_trade_condition(self, dt):
        py_dt = pd.Timestamp(dt).to_pydatetime()
        if py_dt.hour < 10 or py_dt.hour > 14:
            return True
        
        return False
                
class INTRADAY_PULLBACK_PRICE_LB(INTRADAY_PULLBACK):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_PULLBACK_PRICE_LB']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, rsi_period=None, lb_period=None, rsi_exit=None, max_holding=None, trend_baseline=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Start
        self.rsi_period = rsi_period
        self.lb_period = lb_period or 5
        self.rsi_exit = rsi_exit or (55, 45)
        self.max_holding = max_holding or 5
        self.trend_baseline = trend_baseline or 20
        self.min_bars_to_trade = 2   #hardcoded for now
        self.bars_since_trade = None
        self.restrict_trade_time = restrict_trade_time or False
        self._state_vars = {'entry_state': None, 'entry_rsi': None, 'entry_ema': None, 'entry_signal': None, 'entry_price': None, 'bars_since_trade': None, 'prev_state': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['EMA'] = data['EMA']
        self.indicators_to_publish['lb_price_min'] = data['lb_price_min']
        self.indicators_to_publish['lb_price_max'] = data['lb_price_max']
        self.indicators_to_publish['RSI'] = data['RSI']
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        signal = None
        ema = data['EMA']
        rsi = data['RSI']
        lb_price_min = data['lb_price_min']
        lb_price_max = data['lb_price_max']
        price_close = data['{} Close'.format(ticker)]
        buy_signal = price_close > ema and price_close <= lb_price_min and not no_trade
        buy_squareoff = rsi > self.rsi_exit[0] or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        sell_signal = price_close < ema and price_close >= lb_price_max and not no_trade
        sell_squareoff = rsi < self.rsi_exit[1] or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
        
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
        self.extended_mkt['EMA'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.trend_baseline)
        self.extended_mkt['RSI'] = RSI(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.rsi_period)
        self.extended_mkt['lb_price_min'] = self.extended_mkt['{} Close'.format(ticker)].rolling(window=self.lb_period).min()
        self.extended_mkt['lb_price_max'] = self.extended_mkt['{} Close'.format(ticker)].rolling(window=self.lb_period).max()
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_PULLBACK_CUMUL_RSI(INTRADAY_PULLBACK):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_PULLBACK_CUMUL_RSI']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, rsi_period=None, cumul_rsi_period=None, rsi_entry=None, rsi_exit=None, max_holding=None, trend_baseline=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_PULLBACK_CUMUL_RSI, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, rsi_period, rsi_entry, rsi_exit, max_holding, trend_baseline, side_restriction, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app=None)
        self.cumul_rsi_period = cumul_rsi_period
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        ema = data['EMA']
        rsi = data['RSI']
        cumul_rsi = data['Cumul RSI']
        price_close = data['{} Close'.format(ticker)]
        buy_signal = price_close > ema and cumul_rsi <= self.rsi_entry[0] * self.cumul_rsi_period and not no_trade
        buy_squareoff = rsi > self.rsi_exit[0] or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        sell_signal = price_close < ema and cumul_rsi >= self.rsi_entry[1] * self.cumul_rsi_period and not no_trade
        sell_squareoff = rsi < self.rsi_exit[1] or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
        
    def prepare_strategy_attributes(self, dt=None):
        super(INTRADAY_PULLBACK_CUMUL_RSI, self).prepare_strategy_attributes(dt)
        self.extended_mkt['Cumul RSI'] = self.extended_mkt['RSI'].rolling(window=self.cumul_rsi_period).sum()
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_PULLBACK_BB(INTRADAY_PULLBACK):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_PULLBACK_BB']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, bb_period=None, bb_stdev=None, trend_baseline=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Start
        self.bb_period = bb_period
        self.bb_stdev = bb_stdev or 2.0
        self.trend_baseline = trend_baseline or 20
        self.min_bars_to_trade = 2   #hardcoded for now
        self.bars_since_trade = None
        self.restrict_trade_time = restrict_trade_time or False
        self._state_vars = {'entry_state': None, 'entry_rsi': None, 'entry_ema': None, 'entry_signal': None, 'entry_price': None, 'bars_since_trade': None, 'prev_state': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['EMA'] = data['EMA']
        self.indicators_to_publish['BB_upper'] = data['BB_upper']
        self.indicators_to_publish['BB_middle'] = data['BB_middle']
        self.indicators_to_publish['BB_lower'] = data['BB_lower']
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        ema = self.indicators_to_publish['EMA']
        bb_upper = self.indicators_to_publish['BB_upper']
        bb_middle = self.indicators_to_publish['BB_middle']
        bb_lower = self.indicators_to_publish['BB_lower']
        price_close = data['{} Close'.format(ticker)]
        buy_signal = price_close < bb_lower and bb_middle > ema and not no_trade
        buy_squareoff = price_close >= bb_middle or bb_middle <= ema
        sell_signal = price_close > bb_upper and bb_middle < ema and not no_trade
        sell_squareoff = price_close <= bb_middle or bb_middle >= ema
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
        
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
        self.extended_mkt['EMA'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.trend_baseline)
        bb_upper, bb_middle, bb_lower = BBANDS(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.bb_period, nbdevup=self.bb_stdev, nbdevdn=self.bb_stdev)
        self.extended_mkt['BB_upper'] = bb_upper
        self.extended_mkt['BB_middle'] = bb_middle
        self.extended_mkt['BB_lower'] = bb_lower
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
    
class INTRADAY_BB(INTRADAY_PULLBACK):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_BB']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, bb_period=None, bb_stdev=None, max_holding=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Start
        self.bb_period = bb_period
        self.bb_stdev = bb_stdev or 2.0
        self.max_holding = max_holding
        self.min_bars_to_trade = 2   #hardcoded for now
        self.bars_since_trade = None
        self.restrict_trade_time = restrict_trade_time or False
        self._state_vars = {'entry_state': None, 'entry_rsi': None, 'entry_ema': None, 'entry_signal': None, 'entry_price': None, 'bars_since_trade': None, 'prev_state': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['BB_upper'] = data['BB_upper']
        self.indicators_to_publish['BB_middle'] = data['BB_middle']
        self.indicators_to_publish['BB_lower'] = data['BB_lower']
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        signal = None
        bb_upper = self.indicators_to_publish['BB_upper']
        bb_middle = self.indicators_to_publish['BB_middle']
        bb_lower = self.indicators_to_publish['BB_lower']
        price_close = data['{} Close'.format(ticker)]
        buy_signal = price_close < bb_lower and not no_trade
        buy_squareoff = price_close >= bb_middle or (self.max_holding is not None and self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding) or self.max_holding is None
        sell_signal = price_close > bb_upper and not no_trade
        sell_squareoff = price_close <= bb_middle or (self.max_holding is not None and self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding) or self.max_holding is None
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
        
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
        bb_upper, bb_middle, bb_lower = BBANDS(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.bb_period, nbdevup=self.bb_stdev, nbdevdn=self.bb_stdev)
        self.extended_mkt['BB_upper'] = bb_upper
        self.extended_mkt['BB_middle'] = bb_middle
        self.extended_mkt['BB_lower'] = bb_lower
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_PULLBACK_CSTICK_REV(INTRADAY_PULLBACK):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_PULLBACK_CSTICK_REV']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, cstick_modes=None, rsi_period=None, rsi_entry=None, rsi_exit=None, max_holding=None, trend_baseline=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_PULLBACK_CSTICK_REV, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, rsi_period, rsi_entry, rsi_exit, max_holding, trend_baseline, side_restriction, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app=None)
        # 1 - hammer (bull), shooting star (bear), gravestone doji (bear), dragonfly doji (bull)
        # 2 - inverted hammer (bull), hanging man (bear), gravestone doji (bull), dragonfly doji (bear)
        # 3 - morning star (bull), morning doji star (bull), evening star (bear), evening doji star (bear)
        # 4 - bullish engulfing (bull), bearish engulfing (bear)
        # 5 - bullish harami (bull), bearish harami (bear)
        self.cstick_modes = [int(x) for x in cstick_modes.split(",")]
        self.max_holding = max_holding
        self._state_vars['sl_price'] = None
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        ema = data['EMA']
        rsi = data['RSI']
        rsi_m1 = data['RSI_m1']
        rsi_m2 = data['RSI_m2']
        price_close = data['{} Close'.format(ticker)]
        buy_signals = [False, False, False, False, False]
        sell_signals = [False, False, False, False, False]
        any_bull_reversal = data['hammer'] == 100 or data['dragonfly_doji'] == 100 or data['gravestone_doji'] == 100 or data['inverted_hammer'] == 100 or data['morning_star'] == 100 or data['morning_doji_star'] == 100 or data['engulfing'] == 100 or data['harami'] == 100
        any_bear_reversal = data['shooting_star'] == -100 or data['dragonfly_doji'] == 100 or data['gravestone_doji'] == 100 or data['hanging_man'] == -100 or data['evening_star'] == -100 or data['evening_doji_star'] == -100 or data['engulfing'] == -100 or data['harami'] == -100
        if 1 in self.cstick_modes:
            is_bull_reversal = data['hammer'] == 100 or data['dragonfly_doji'] == 100
            is_bear_reversal = data['shooting_star'] == -100 or data['gravestone_doji'] == 100
            buy_signals[0] = price_close > ema and rsi_m1 < self.rsi_entry[0] and is_bull_reversal and not no_trade
            sell_signals[0] = price_close < ema and rsi_m1 > self.rsi_entry[1] and is_bear_reversal and not no_trade
        if 2 in self.cstick_modes:
            is_bull_reversal = data['inverted_hammer'] == 100 or data['gravestone_doji'] == 100
            is_bear_reversal = data['hanging_man'] == -100 or data['dragonfly_doji'] == 100
            buy_signals[1] = price_close > ema and rsi_m1 < self.rsi_entry[0] and is_bull_reversal and not no_trade
            sell_signals[1] = price_close < ema and rsi_m1 > self.rsi_entry[1] and is_bear_reversal and not no_trade
        if 3 in self.cstick_modes:
            is_bull_reversal = data['morning_star'] == 100 or data['morning_doji_star'] == 100
            is_bear_reversal = data['evening_star'] == -100 or data['evening_doji_star'] == -100
            buy_signals[2] = price_close > ema and min(rsi_m1, rsi_m2) < self.rsi_entry[0] and is_bull_reversal and not no_trade
            sell_signals[2] = price_close < ema and max(rsi_m1, rsi_m2) > self.rsi_entry[1] and is_bear_reversal and not no_trade
        if 4 in self.cstick_modes:
            is_bull_reversal = data['engulfing'] == 100
            is_bear_reversal = data['engulfing'] == -100
            buy_signals[3] = price_close > ema and rsi_m1 < self.rsi_entry[0] and is_bull_reversal and not no_trade
            sell_signals[3] = price_close < ema and rsi_m1 > self.rsi_entry[1] and is_bear_reversal and not no_trade
        if 5 in self.cstick_modes:
            is_bull_reversal = data['harami'] == 100
            is_bear_reversal = data['harami'] == -100
            buy_signals[4] = price_close > ema and rsi_m1 < self.rsi_entry[0] and is_bull_reversal and not no_trade
            sell_signals[4] = price_close < ema and rsi_m1 > self.rsi_entry[1] and is_bear_reversal and not no_trade
        buy_signal = True if True in buy_signals else False
        sell_signal = True if True in sell_signals else False
        if self.max_holding is not None:
            buy_squareoff = rsi > self.rsi_exit[0] or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
            sell_squareoff = rsi < self.rsi_exit[1] or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        else:
            buy_squareoff = any_bear_reversal or (self._state_vars['sl_price'] is not None and price_close < self._state_vars['sl_price'])
            sell_squareoff = any_bull_reversal or (self._state_vars['sl_price'] is not None and price_close > self._state_vars['sl_price'])
            self._update_sl_price(data, buy_signal, buy_squareoff, sell_signal, sell_squareoff)
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
        
    def prepare_strategy_attributes(self, dt=None):
        super(INTRADAY_PULLBACK_CSTICK_REV, self).prepare_strategy_attributes(dt)
        ticker = self.tickers[0]
        o = '{} Open'.format(ticker)
        h = '{} High'.format(ticker)
        l = '{} Low'.format(ticker)
        c = '{} Close'.format(ticker)
        o_ser = self.extended_mkt.loc[:, o]
        h_ser = self.extended_mkt.loc[:, h]
        l_ser = self.extended_mkt.loc[:, l]
        c_ser = self.extended_mkt.loc[:, c]
        self.extended_mkt['RSI_m1'] = self.extended_mkt.loc[:, 'RSI'].shift(1)
        self.extended_mkt['RSI_m2'] = self.extended_mkt.loc[:, 'RSI'].shift(2)
        #self.extended_mkt['RSI_m3'] = self.extended_mkt.loc[:, 'RSI'].shift(3)
        self.extended_mkt['hammer'] = CDLHAMMER(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['shooting_star'] = CDLSHOOTINGSTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['gravestone_doji'] = CDLGRAVESTONEDOJI(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['dragonfly_doji'] = CDLDRAGONFLYDOJI(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['inverted_hammer'] = CDLINVERTEDHAMMER(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['hanging_man'] = CDLHANGINGMAN(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['morning_star'] = CDLMORNINGSTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['morning_doji_star'] = CDLMORNINGDOJISTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['evening_star'] = CDLEVENINGSTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['evening_doji_star'] = CDLEVENINGDOJISTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['engulfing'] = CDLENGULFING(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['harami'] = CDLHARAMI(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['EMA'] = data['EMA']
        self.indicators_to_publish['RSI'] = data['RSI']
        self.indicators_to_publish['RSI_m1'] = data['RSI_m1']
        self.indicators_to_publish['RSI_m2'] = data['RSI_m2']
        self.indicators_to_publish['hammer'] = data['hammer']
        self.indicators_to_publish['shooting_star'] = data['shooting_star']
        self.indicators_to_publish['gravestone_doji'] = data['gravestone_doji']
        self.indicators_to_publish['dragonfly_doji'] = data['dragonfly_doji']
        self.indicators_to_publish['inverted_hammer'] = data['inverted_hammer']
        self.indicators_to_publish['hanging_man'] = data['hanging_man']
        self.indicators_to_publish['morning_star'] = data['morning_star']
        self.indicators_to_publish['morning_doji_star'] = data['morning_doji_star']
        self.indicators_to_publish['evening_star'] = data['evening_star']
        self.indicators_to_publish['evening_doji_star'] = data['evening_doji_star']
        self.indicators_to_publish['engulfing'] = data['engulfing']
        self.indicators_to_publish['harami'] = data['harami']
        self.indicators_to_publish['sl_price'] = self._state_vars['sl_price']
        
    def _update_sl_price(self, data, buy_signal, buy_squareoff, sell_signal, sell_squareoff):
        ticker = self.tickers[0]
        if self.trade_state == self.TRADE_STATES.Intraday_squareoff:
            if buy_signal:
                self._state_vars['sl_price'] = data['{} Low'.format(ticker)]
            elif sell_signal:
                self._state_vars['sl_price'] = data['{} High'.format(ticker)]
        elif self.trade_state == self.TRADE_STATES.Regular_buy:
            if buy_squareoff:
                self._state_vars['sl_price'] = None
        elif self.trade_state == self.TRADE_STATES.Regular_sell:
            if sell_squareoff:
                self._state_vars['sl_price'] = None
    