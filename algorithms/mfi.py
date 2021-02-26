from utility import av_call, get_df_from_av_json
from algorithms.tradingstrategy import TradingStrategy
import pandas as pd

class MFI(TradingStrategy):
    def __init__(self, lower=20, upper=80, period=14, preinit={}):
        self.name = "mfi"
        if len(preinit) == 0:
            self.lower = lower # Lower cutoff for MFI (used to determine when to buy)
            self.upper = upper # Upper cutoff for MFI (used to determine when to sell)
            self.period = str(period) # Time period for which MFI is calculated for
        
        else:
            self.lower = preinit['lower']
            self.upper = preinit['upper']
            self.period = preinit['period']
    
    def get_signals(self, symbols):
        """
        Gets which holdings to buy, sell, and continue holding
        """
        buy = []
        sell = []
        hold = []
        for ticker in symbols:
            params = {
                'symbol' : ticker,
                'interval' : 'daily',
                'time_period' : self.period
            }
            mfijson = av_call('MFI', params)
            mfi = get_df_from_av_json(mfijson)
            if mfi['MFI'][-1] > self.upper:
                sell.append(ticker)
            elif mfi['MFI'][-1] < self.lower:
                buy.append(ticker)
            else:
                hold.append(ticker)
        return {
            'buy': buy,
            'sell': sell,
            'hold': hold
        }
        