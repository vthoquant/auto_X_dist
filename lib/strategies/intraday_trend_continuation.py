# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 13:07:13 2022

@author: vivin
"""
from lib.strategies.intraday_pullback import INTRADAY_PULLBACK
from lib.configs.directory_names import STRATEGY_RUN_BASE_PATHS
from talib.abstract import CDLGRAVESTONEDOJI, CDLDRAGONFLYDOJI, CDLINVERTEDHAMMER, CDLHANGINGMAN, CDLMORNINGDOJISTAR, CDLMORNINGSTAR, CDLEVENINGDOJISTAR, CDLEVENINGSTAR, CDLENGULFING, CDLDOJI, CDLDOJISTAR, CDLSPINNINGTOP, CDL3BLACKCROWS, CDLRISEFALL3METHODS, ATR

class INTRADAY_CONTINUATION_HLDG(INTRADAY_PULLBACK):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_CONTINUATION_HLDG']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, cstick_modes=None, rsi_period=None, rsi_entry=None, max_holding=None, trend_baseline=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_CONTINUATION_HLDG, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, rsi_period, rsi_entry, None, max_holding, trend_baseline, side_restriction, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app)
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
        signal, buy_signal, sell_signal = self._get_buysell_signals(data, dt)
        ticker = self.tickers[0]
        price_close = data['{} Close'.format(ticker)]
        ema = data['EMA']
        if self.max_holding is not None:
            buy_squareoff = self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding
            sell_squareoff = self.bars_since_trade is not None and self.bars_since_trade >= self.max_holding
        else:
            buy_squareoff = price_close < ema
            sell_squareoff = price_close > ema
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
    
    def _get_buysell_signals(self, data, dt):
        no_trade = False if not self.restrict_trade_time else self._no_trade_condition(dt)
        ticker = self.tickers[0]
        signal = None
        ema = data['EMA']
        rsi = data['RSI']
        rsi_m1 = data['RSI_m1']
        rsi_m2 = data['RSI_m2']
        rsi_m3 = data['RSI_m3']
        price_close = data['{} Close'.format(ticker)]
        buy_signals = [False, False, False, False, False]
        sell_signals = [False, False, False, False, False]
        if 1 in self.cstick_modes:
            is_bull_cont = data['hanging_man'] == -100 or data['dragonfly_doji'] == 100 or data['doji'] == 100 or data['doji_star'] == 100 or data['spinning_top'] == 100 or data['spinning_top'] == -100
            is_bear_cont = data['inverted_hammer'] == -100 or data['gravestone_doji'] == 100 or data['doji'] == 100 or data['doji_star'] == 100 or data['spinning_top'] == -100 or data['spinning_top'] == 100
            buy_signals[0] = price_close > ema and max(rsi, rsi_m1) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[0] = price_close < ema and min(rsi, rsi_m1) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 2 in self.cstick_modes:
            is_bull_cont = data['evening_star'] == -100 or data['evening_doji_star'] == -100
            is_bear_cont = data['morning_star'] == 100 or data['morning_doji_star'] == 100
            buy_signals[1] = price_close > ema and max(rsi_m1, rsi_m2) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[1] = price_close < ema and min(rsi_m1, rsi_m2) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 3 in self.cstick_modes:
            is_bull_cont = data['engulfing'] == -100
            is_bear_cont = data['engulfing'] == 100
            buy_signals[2] = price_close > ema and rsi_m1 > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[2] = price_close < ema and rsi_m1 < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 4 in self.cstick_modes:
            is_bull_cont = data['rise_fall_three'] == 100
            is_bear_cont = data['rise_fall_three'] == -100
            buy_signals[3] = price_close > ema and max(rsi, rsi_m1, rsi_m2, rsi_m3) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[3] = price_close < ema and min(rsi, rsi_m1, rsi_m2, rsi_m3) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 5 in self.cstick_modes:
            is_bull_cont = data['three_black_crows'] == 100
            is_bear_cont = data['three_black_crows'] == -100
            buy_signals[4] = price_close > ema and max(rsi, rsi_m1) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[4] = price_close < ema and min(rsi, rsi_m1) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 6 in self.cstick_modes:
            is_bull_cont = data['hanging_man'] == -100 or data['dragonfly_doji'] == 100
            is_bear_cont = data['inverted_hammer'] == -100 or data['gravestone_doji'] == 100
            buy_signals[0] = price_close > ema and max(rsi, rsi_m1) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[0] = price_close < ema and min(rsi, rsi_m1) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 7 in self.cstick_modes:
            is_bull_cont = data['doji'] == 100 or data['doji_star'] == 100
            is_bear_cont = data['doji'] == 100 or data['doji_star'] == 100
            buy_signals[0] = price_close > ema and max(rsi, rsi_m1) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[0] = price_close < ema and min(rsi, rsi_m1) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 8 in self.cstick_modes:
            is_bull_cont = data['spinning_top'] == 100 or data['spinning_top'] == -100
            is_bear_cont = data['spinning_top'] == -100 or data['spinning_top'] == 100
            buy_signals[0] = price_close > ema and max(rsi, rsi_m1) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[0] = price_close < ema and min(rsi, rsi_m1) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 9 in self.cstick_modes:
            is_bull_cont = data['spinning_top'] == 100 
            is_bear_cont = data['spinning_top'] == -100
            buy_signals[0] = price_close > ema and max(rsi, rsi_m1) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[0] = price_close < ema and min(rsi, rsi_m1) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 10 in self.cstick_modes:
            is_bull_cont = data['spinning_top'] == -100
            is_bear_cont = data['spinning_top'] == 100
            buy_signals[0] = price_close > ema and max(rsi, rsi_m1) > self.rsi_entry[0] and is_bull_cont and not no_trade
            sell_signals[0] = price_close < ema and min(rsi, rsi_m1) < self.rsi_entry[1] and is_bear_cont and not no_trade
        if 0 in self.cstick_modes:
            buy_signals[0] = price_close > ema and rsi > self.rsi_entry[0]
            sell_signals[0] = price_close < ema and rsi < self.rsi_entry[1]
        buy_signal = True if True in buy_signals else False
        sell_signal = True if True in sell_signals else False
        return signal, buy_signal, sell_signal
        
    def prepare_strategy_attributes(self, dt=None):
        super(INTRADAY_CONTINUATION_HLDG, self).prepare_strategy_attributes(dt)
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
        self.extended_mkt['RSI_m3'] = self.extended_mkt.loc[:, 'RSI'].shift(3)
        self.extended_mkt['ATR'] = ATR(h_ser, l_ser, c_ser)
        self.extended_mkt['doji'] = CDLDOJI(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['doji_star'] = CDLDOJISTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['spinning_top'] = CDLSPINNINGTOP(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['gravestone_doji'] = CDLGRAVESTONEDOJI(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['dragonfly_doji'] = CDLDRAGONFLYDOJI(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['inverted_hammer'] = CDLINVERTEDHAMMER(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['hanging_man'] = CDLHANGINGMAN(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['morning_star'] = CDLMORNINGSTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['morning_doji_star'] = CDLMORNINGDOJISTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['evening_star'] = CDLEVENINGSTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['evening_doji_star'] = CDLEVENINGDOJISTAR(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['engulfing'] = CDLENGULFING(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['rise_fall_three'] = CDLRISEFALL3METHODS(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt['three_black_crows'] = CDL3BLACKCROWS(o_ser, h_ser, l_ser, c_ser)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['EMA'] = data['EMA']
        self.indicators_to_publish['RSI'] = data['RSI']
        self.indicators_to_publish['RSI_m1'] = data['RSI_m1']
        self.indicators_to_publish['RSI_m2'] = data['RSI_m2']
        self.indicators_to_publish['RSI_m3'] = data['RSI_m3']
        self.indicators_to_publish['ATR'] = data['ATR']
        self.indicators_to_publish['doji'] = data['doji']
        self.indicators_to_publish['doji_star'] = data['doji_star']
        self.indicators_to_publish['spinning_top'] = data['spinning_top']
        self.indicators_to_publish['gravestone_doji'] = data['gravestone_doji']
        self.indicators_to_publish['dragonfly_doji'] = data['dragonfly_doji']
        self.indicators_to_publish['inverted_hammer'] = data['inverted_hammer']
        self.indicators_to_publish['hanging_man'] = data['hanging_man']
        self.indicators_to_publish['morning_star'] = data['morning_star']
        self.indicators_to_publish['morning_doji_star'] = data['morning_doji_star']
        self.indicators_to_publish['evening_star'] = data['evening_star']
        self.indicators_to_publish['evening_doji_star'] = data['evening_doji_star']
        self.indicators_to_publish['engulfing'] = data['engulfing']
        self.indicators_to_publish['rise_fall_three'] = data['rise_fall_three']
        self.indicators_to_publish['three_black_crows'] = data['three_black_crows']
        
class INTRADAY_CONTINUATION_ATRTP(INTRADAY_CONTINUATION_HLDG):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_CONTINUATION_ATRTP']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, cstick_modes=None, rsi_period=None, rsi_entry=None, atr_tp=None, trend_baseline=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_CONTINUATION_ATRTP, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, cstick_modes, rsi_period, rsi_entry, None, trend_baseline, side_restriction, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app)
        self.atr_tp = atr_tp
        self._state_vars['entry_price'] = None
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        signal, buy_signal, sell_signal = self._get_buysell_signals(data, dt)
        ticker = self.tickers[0]
        price_close = data['{} Close'.format(ticker)]
        ema = data['EMA']
        atr = data['ATR']
        if ema is not None and self._state_vars['entry_price'] is not None:
            buy_squareoff = (price_close >= (self._state_vars['entry_price'] + self.atr_tp * atr)) or (price_close < ema)
            sell_squareoff = (price_close <= (self._state_vars['entry_price'] - self.atr_tp * atr)) or (price_close > ema)
        else:
            buy_squareoff, sell_squareoff = False, False
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
    
    def _update_indicators_to_publish(self, data):
        super(INTRADAY_CONTINUATION_ATRTP, self)._update_indicators_to_publish(data)
        atr = data['ATR']
        self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
        self.indicators_to_publish['tp_level_long'] = self._state_vars['entry_price'] + self.atr_tp * atr if atr is not None and self._state_vars['entry_price'] is not None else None
        self.indicators_to_publish['tp_level_short'] = self._state_vars['entry_price'] - self.atr_tp * atr if atr is not None and self._state_vars['entry_price'] is not None else None
    
class INTRADAY_CONTINUATION_ATRSLSHIFT(INTRADAY_CONTINUATION_HLDG):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_CONTINUATION_ATRSLSHIFT']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, cstick_modes=None, rsi_period=None, rsi_entry=None, atr_tp=None, trend_baseline=None, side_restriction=None, rescale_shorts=False, restrict_trade_time=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_CONTINUATION_ATRSLSHIFT, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, cstick_modes, rsi_period, rsi_entry, None, trend_baseline, side_restriction, rescale_shorts, restrict_trade_time, add_transaction_costs, inst_delta, app)
        self.atr_tp = atr_tp
        self._state_vars['entry_price'] = None
        self._long_sl_shifted = False
        self._short_sl_shifted = False
        self._long_sl = None
        self._short_sl = None
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        signal, buy_signal, sell_signal = self._get_buysell_signals(data, dt)
        ticker = self.tickers[0]
        price_close = data['{} Close'.format(ticker)]
        ema = data['EMA']
        atr = data['ATR']
        self._update_current_sl(price_close, atr, ema)
        buy_squareoff = (price_close < self._long_sl) if self._long_sl is not None else False
        sell_squareoff = (price_close > self._short_sl) if self._short_sl is not None else False
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
    
    def _update_current_sl(self, price_close, atr, ema):
        if self.trade_state != self.TRADE_STATES.Regular_buy:
            self._long_sl_shifted = False
            self._long_sl = None
        if self.trade_state != self.TRADE_STATES.Regular_sell:
            self._short_sl_shifted = False
            self._short_sl = None
        if self.trade_state == self.TRADE_STATES.Regular_buy:
            self._long_sl = ema
            if (price_close > self._state_vars['entry_price'] + self.atr_tp * atr) and not self._long_sl_shifted:
                self._long_sl = self._state_vars['entry_price']
                self._long_sl_shifted = True
            if self._long_sl_shifted:
                self._long_sl = max(self._state_vars['entry_price'], ema)
        if self.trade_state == self.TRADE_STATES.Regular_sell:
            self._short_sl = ema
            if (price_close < self._state_vars['entry_price'] - self.atr_tp * atr) and not self._short_sl_shifted:
                self._short_sl = self._state_vars['entry_price']
                self._short_sl_shifted = True
            if self._short_sl_shifted:
                self._short_sl = min(self._state_vars['entry_price'], ema)
                
    def _update_indicators_to_publish(self, data):
        super(INTRADAY_CONTINUATION_ATRSLSHIFT, self)._update_indicators_to_publish(data)
        atr = data['ATR']
        self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
        self.indicators_to_publish['tp_level_long'] = self._state_vars['entry_price'] + self.atr_tp * atr if atr is not None and self._state_vars['entry_price'] is not None else None
        self.indicators_to_publish['tp_level_short'] = self._state_vars['entry_price'] - self.atr_tp * atr if atr is not None and self._state_vars['entry_price'] is not None else None
        self.indicators_to_publish['short_sl'] = self._short_sl
        self.indicators_to_publish['long_sl'] = self._long_sl
        