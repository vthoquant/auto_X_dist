# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 13:10:49 2021

@author: vivin
"""
from lib.strategies.base_classes import INTRADAY_BASE
from lib.strategies.intraday_pullback import INTRADAY_PULLBACK, INTRADAY_PULLBACK_BB, INTRADAY_PULLBACK_PRICE_LB, INTRADAY_PULLBACK_CSTICK_REV
from lib.configs.directory_names import STRATEGY_RUN_BASE_PATHS
import pandas as pd
import numpy as np
from talib.abstract import ROCP, RSI, EMA, CCI, ATR
import datetime

class INTRADAY_OVERTRADE_RSI(INTRADAY_PULLBACK):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_OVERTRADE_RSI']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, rsi_period=None, rsi_entry=None, rsi_exit=None, max_holding=None, trend_baseline_short=None, trend_baseline_long=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_OVERTRADE_RSI, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, rsi_period, rsi_entry, rsi_exit, max_holding, None, side_restriction, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app)
        self.trend_baseline_long = trend_baseline_long
        self.trend_baseline_short = trend_baseline_short

    def _generate_trade_conditions(self, data, dt):
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_PULLBACK.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        price_close = data['{} Close'.format(ticker)]
        ema_long = data['EMA_long']
        ema_short = data['EMA_short']
        rsi = data['RSI']
        buy_signal = price_close <= ema_short and rsi < self.rsi_entry[0] and (ema_short <= ema_long or self.trend_baseline_long is None) and not no_trade
        buy_squareoff = rsi > self.rsi_exit[0] or price_close > ema_short or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        sell_signal = price_close >= ema_short and rsi > self.rsi_entry[1] and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
        sell_squareoff = rsi < self.rsi_exit[1] or price_close < ema_short or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
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
        self.extended_mkt['EMA_long'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=(self.trend_baseline_long or 100))
        self.extended_mkt['EMA_short'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.trend_baseline_short)
        self.extended_mkt['RSI'] = RSI(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.rsi_period)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['EMA_short'] = data['EMA_short']
        self.indicators_to_publish['EMA_long'] = data['EMA_long']
        self.indicators_to_publish['RSI'] = data['RSI']
        
class INTRADAY_OVERTRADE_CUMUL_RSI(INTRADAY_OVERTRADE_RSI):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_OVERTRADE_CUMUL_RSI']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, rsi_period=None, rsi_entry=None, rsi_exit=None, cumul_rsi_period=None, max_holding=None, trend_baseline_short=None, trend_baseline_long=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_OVERTRADE_CUMUL_RSI, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, rsi_period, rsi_entry, rsi_exit, max_holding, trend_baseline_short, trend_baseline_long, side_restriction, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app)
        self.cumul_rsi_period = cumul_rsi_period
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_PULLBACK.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        price_close = data['{} Close'.format(ticker)]
        ema_long = data['EMA_long']
        ema_short = data['EMA_short']
        rsi = data['RSI']
        cumul_rsi = data['Cumul RSI']
        buy_signal = price_close <= ema_short and cumul_rsi < self.rsi_entry[0] * self.cumul_rsi_period and (ema_short <= ema_long or self.trend_baseline_long is None) and not no_trade
        buy_squareoff = rsi > self.rsi_exit[0] or price_close > ema_short or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        sell_signal = price_close >= ema_short and cumul_rsi > self.rsi_entry[1] * self.cumul_rsi_period and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
        sell_squareoff = rsi < self.rsi_exit[1] or price_close < ema_short or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
        
    def prepare_strategy_attributes(self, dt=None):
        super(INTRADAY_OVERTRADE_CUMUL_RSI, self).prepare_strategy_attributes(dt)
        self.extended_mkt['Cumul RSI'] = self.extended_mkt['RSI'].rolling(window=self.cumul_rsi_period).sum()
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _update_indicators_to_publish(self, data):
        super(INTRADAY_OVERTRADE_CUMUL_RSI, self)._update_indicators_to_publish(data)
        self.indicators_to_publish['Cumul RSI'] = data['Cumul RSI']
    
class INTRADAY_OVERTRADE_PRICE_LB(INTRADAY_PULLBACK_PRICE_LB):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_OVERTRADE_PRICE_LB']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, rsi_period=None, lb_period=None, rsi_exit=None, max_holding=None, trend_baseline_long=None, trend_baseline_short=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_OVERTRADE_PRICE_LB, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, rsi_period, lb_period, rsi_exit, max_holding, None, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app)
        self.trend_baseline_long = trend_baseline_long
        self.trend_baseline_short = trend_baseline_short
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['EMA_short'] = data['EMA_short']
        self.indicators_to_publish['EMA_long'] = data['EMA_long']
        self.indicators_to_publish['lb_price_min'] = data['lb_price_min']
        self.indicators_to_publish['lb_price_max'] = data['lb_price_max']
        self.indicators_to_publish['RSI'] = data['RSI']
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        ema_short = data['EMA_short']
        ema_long = data['EMA_long']
        rsi = data['RSI']
        lb_price_min = data['lb_price_min']
        lb_price_max = data['lb_price_max']
        price_close = data['{} Close'.format(ticker)]
        buy_signal = price_close < ema_short and price_close <= lb_price_min and (ema_short <= ema_long or self.trend_baseline_long is None) and not no_trade
        buy_squareoff = rsi > self.rsi_exit[0] or price_close >= ema_short or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        sell_signal = price_close > ema_short and price_close >= lb_price_max and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
        sell_squareoff = rsi < self.rsi_exit[1] or price_close <= ema_short or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
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
        self.extended_mkt['EMA_long'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=(self.trend_baseline_long or 100))
        self.extended_mkt['EMA_short'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.trend_baseline_short)
        self.extended_mkt['RSI'] = RSI(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.rsi_period)
        self.extended_mkt['lb_price_min'] = self.extended_mkt['{} Close'.format(ticker)].rolling(window=self.lb_period).min()
        self.extended_mkt['lb_price_max'] = self.extended_mkt['{} Close'.format(ticker)].rolling(window=self.lb_period).max()
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_OVERTRADE_BB(INTRADAY_PULLBACK_BB):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_OVERTRADE_BB']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, bb_period=None, bb_stdev=None, trend_baseline=None, max_holding=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_OVERTRADE_BB, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, bb_period, bb_stdev, trend_baseline, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app)
        self.max_holding = max_holding
        
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
        buy_signal = price_close < bb_lower and bb_middle < ema and not no_trade
        buy_squareoff = price_close >= bb_middle or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        sell_signal = price_close > bb_upper and bb_middle > ema and not no_trade
        sell_squareoff = price_close <= bb_middle or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
    
class INTRADAY_OVERTRADE_RSI_CSTICK_REV(INTRADAY_PULLBACK_CSTICK_REV):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_OVERTRADE_RSI_CSTICK_REV']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, cstick_modes=None, rsi_period=None, rsi_entry=None, rsi_exit=None, max_holding=None, trend_baseline_short=None, trend_baseline_long=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_OVERTRADE_RSI_CSTICK_REV, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, cstick_modes, rsi_period, rsi_entry, rsi_exit, max_holding, trend_baseline_long, side_restriction, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app)
        # self.trend_baseline is set to trend_baseline_long so that we can just directly used the inherited method
        self.trend_baseline_long = trend_baseline_long
        self.trend_baseline_short = trend_baseline_short
        self.max_holding = max_holding

    def _generate_trade_conditions2(self, data, dt):
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_PULLBACK.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        price_close = data['{} Close'.format(ticker)]
        ema_long = data['EMA_long']
        ema_short = data['EMA_short']
        rsi = data['RSI']
        buy_signal = price_close <= ema_short and rsi < self.rsi_entry[0] and (ema_short <= ema_long or self.trend_baseline_long is None) and not no_trade
        buy_squareoff = rsi > self.rsi_exit[0] or price_close > ema_short or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        sell_signal = price_close >= ema_short and rsi > self.rsi_entry[1] and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
        sell_squareoff = rsi < self.rsi_exit[1] or price_close < ema_short or (self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding)
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
    
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        ema_long = data['EMA_long']
        ema_short = data['EMA_short']
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
            buy_signals[0] = price_close <= ema_short and rsi_m1 < self.rsi_entry[0] and is_bull_reversal and (ema_short <= ema_long or self.trend_baseline_long is None) and not no_trade
            sell_signals[0] = price_close >= ema_short and rsi_m1 > self.rsi_entry[1] and is_bear_reversal and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
        if 2 in self.cstick_modes:
            is_bull_reversal = data['inverted_hammer'] == 100 or data['gravestone_doji'] == 100
            is_bear_reversal = data['hanging_man'] == -100 or data['dragonfly_doji'] == 100
            buy_signals[1] = price_close <= ema_short and rsi_m1 < self.rsi_entry[0] and is_bull_reversal and (ema_short <= ema_long or self.trend_baseline_long is None) and not no_trade
            sell_signals[1] = price_close >= ema_short and rsi_m1 > self.rsi_entry[1] and is_bear_reversal and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
        if 3 in self.cstick_modes:
            is_bull_reversal = data['morning_star'] == 100 or data['morning_doji_star'] == 100
            is_bear_reversal = data['evening_star'] == -100 or data['evening_doji_star'] == -100
            buy_signals[2] = price_close <= ema_short and min(rsi_m1, rsi_m2) < self.rsi_entry[0] and is_bull_reversal and (ema_short <= ema_long or self.trend_baseline_long is None) and not no_trade
            sell_signals[2] = price_close >= ema_short and max(rsi_m1, rsi_m2) > self.rsi_entry[1] and is_bear_reversal and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
        if 4 in self.cstick_modes:
            is_bull_reversal = data['engulfing'] == 100
            is_bear_reversal = data['engulfing'] == -100
            buy_signals[3] = price_close <= ema_short and rsi_m1 < self.rsi_entry[0] and is_bull_reversal and (ema_short <= ema_long or self.trend_baseline_long is None) and not no_trade
            sell_signals[3] = price_close >= ema_short and rsi_m1 > self.rsi_entry[1] and is_bear_reversal and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
        if 5 in self.cstick_modes:
            is_bull_reversal = data['harami'] == 100
            is_bear_reversal = data['harami'] == -100
            buy_signals[4] = price_close <= ema_short and rsi_m1 < self.rsi_entry[0] and is_bull_reversal and (ema_short <= ema_long or self.trend_baseline_long is None) and is_bull_reversal and not no_trade
            sell_signals[4] = price_close >= ema_short and rsi_m1 > self.rsi_entry[1] and is_bear_reversal and (ema_short >= ema_long or self.trend_baseline_long is None) and not no_trade
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
        super(INTRADAY_OVERTRADE_RSI_CSTICK_REV, self).prepare_strategy_attributes(dt)
        ticker = self.tickers[0]
        self.extended_mkt['EMA_long'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=(self.trend_baseline_long or 100))
        self.extended_mkt['EMA_short'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.trend_baseline_short)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _update_indicators_to_publish(self, data):
        super(INTRADAY_OVERTRADE_RSI_CSTICK_REV, self)._update_indicators_to_publish(data)
        self.indicators_to_publish['EMA_short'] = data['EMA_short']
        self.indicators_to_publish['EMA_long'] = data['EMA_long']
        
class INTRADAY_HA_CCI(INTRADAY_BASE):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_HA_CCI']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, cci_period=None, cci_entry=None, cci_exit=None, sl_atr=None, tp_atr=None, is_trailing_sl=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = INTRADAY_HA_CCI.TRADE_STATES.Start
        self.cci_period = cci_period
        self.cci_entry = cci_entry or (-100, 100)
        self.cci_exit = cci_exit or (100, -100)
        self.is_trailing_sl = is_trailing_sl or False
        self.sl_atr = sl_atr or 1.0
        self.tp_atr = tp_atr or 1.0
        self.side_restriction = side_restriction
        self.min_bars_to_trade = 2   #hardcoded for now
        self.bars_since_trade = None
        self.restrict_trade_time = restrict_trade_time or False
        self._state_vars = {'entry_state': None, 'entry_signal': None, 'entry_price': None, 'trailing_price': None, 'prev_state': None, 'is_buy_stopped': False, 'is_sell_stopped': False, 'curr_cci': None}
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
            self.indicators_to_publish['is_buy_stopped'] = None
            self.indicators_to_publish['is_sell_stopped'] = None
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['Open_HA'] = data['Open_HA']
        self.indicators_to_publish['High_HA'] = data['High_HA']
        self.indicators_to_publish['Low_HA'] = data['Low_HA']
        self.indicators_to_publish['Close_HA'] = data['Close_HA']
        
        self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
        self.indicators_to_publish['trailing_price'] = self._state_vars['trailing_price']
        self.indicators_to_publish['CCI'] = data['CCI']
        self.indicators_to_publish['ATR'] = data['ATR']
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff = self._generate_trade_conditions(data, dt)
        is_trade_bar = self._process_conditions(data, dt, signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff, isEOD)
        return is_trade_bar
    
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = INTRADAY_PULLBACK.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_PULLBACK.TRADE_STATES.Start else self.trade_state
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        cci = data['CCI']
        self._state_vars['curr_cci'] = cci
        atr = data['ATR']
        price_close = data['{} Close'.format(ticker)]
        price_trailing = self._state_vars['trailing_price']
        price_entry = self._state_vars['entry_price']
        sl_hit_price = price_entry if not self.is_trailing_sl else price_trailing
        buy_signal = cci < self.cci_entry[0] and not no_trade
        buy_squareoff = cci > self.cci_exit[0] or (price_entry is not None and ((price_close - price_entry > atr * self.tp_atr) or (price_close - sl_hit_price < -atr * self.sl_atr)))
        sell_signal = cci > self.cci_entry[1] and not no_trade
        sell_squareoff = cci < self.cci_exit[1] or (price_entry is not None and ((price_close - price_entry < -atr * self.tp_atr) or (price_close - sl_hit_price > atr * self.sl_atr)))
        if self.trade_state == self.TRADE_STATES.Regular_buy:
            self._state_vars['is_buy_stopped'] = price_entry is not None and (price_close - sl_hit_price < -atr * self.sl_atr)
        if self.trade_state == self.TRADE_STATES.Regular_sell:
            self._state_vars['is_sell_stopped'] = price_entry is not None and (price_close - sl_hit_price > atr * self.sl_atr)
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
                if buy_signal and not self._state_vars['is_buy_stopped']:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
                elif sell_signal and not self._state_vars['is_sell_stopped']:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
                else:
                    if self._state_vars['is_buy_stopped'] and self._state_vars['curr_cci'] > self.cci_entry[0]:
                        self._state_vars['is_buy_stopped'] = False
                    elif self._state_vars['is_sell_stopped'] and self._state_vars['curr_cci'] < self.cci_entry[1]:
                        self._state_vars['is_sell_stopped'] = False
            elif self.trade_state == self.TRADE_STATES.Regular_buy:
                if sell_signal:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                elif buy_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self._state_vars['entry_price'] = None
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
                    self._state_vars['trailing_price'] = max(self._state_vars['trailing_price'], price_close)
            elif self.trade_state == self.TRADE_STATES.Regular_sell:
                if buy_signal:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                elif sell_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self._state_vars['entry_price'] = None
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
            self._state_vars['is_buy_stopped'] = False
            self._state_vars['is_sell_stopped'] = False
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        self.indicators_to_publish['is_buy_stopped'] = self._state_vars['is_buy_stopped']
        self.indicators_to_publish['is_sell_stopped'] = self._state_vars['is_sell_stopped']
        
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
        
        self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt[c], timeperiod=1)
        self.extended_mkt['CCI'] = CCI(ha_ext['High_HA'], ha_ext['Low_HA'], ha_ext['Close_HA'], timeperiod=self.cci_period)
        self.extended_mkt['ATR'] = ATR(self.extended_mkt['{} High'.format(ticker)], self.extended_mkt['{} Low'.format(ticker)], self.extended_mkt['{} Close'.format(ticker)])
        
        self.extended_mkt = pd.concat([self.extended_mkt, ha_ext], axis=1)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _no_trade_condition(self, dt):
        py_dt = pd.Timestamp(dt).to_pydatetime()
        if py_dt.hour < 10 or py_dt.hour > 14:
            return True
        
        return False