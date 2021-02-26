from utility import av_call, get_df_from_av_json
from algorithms.tradingstrategy import TradingStrategy
import pandas as pd

class MACD(TradingStrategy):
    def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9, preinit = {}):
        self.name = "macd"
        if len(preinit) == 0:
            self.fastperiod = str(fastperiod) # Fast period used for generating MACD
            self.slowperiod = str(slowperiod) # Slow period used for generating MACD
            self.signalperiod = str(signalperiod) # Signal period used for generating MACD signal line
            self.bought = False
        else: # Dictionary passed in with preinitializations (loading from database)
            self.fastperiod = preinit['fastperiod']
            self.slowperiod = preinit['slowperiod']
            self.signalperiod = preinit['signalperiod']
            self.bought = preinit['bought']
        
    
    def get_signals(self, symbols):
        """
        Gets which holdings to buy, sell, and continue holding
        """
        buy = []
        sell = []
        hold = []
        for ticker in symbols:
            print(ticker)
            params = {
                'symbol' : ticker,
                'interval' : 'daily',
                'series_type' : 'close',
                'fastperiod': self.fastperiod,
                'slowperiod':self.slowperiod,
                'signalperiod':self.signalperiod
            }
            macdjson = av_call('MACD', params)

            if ticker == 'AMGN':
                print(macdjson)

            macd = get_df_from_av_json(macdjson)
            if macd['MACD'][-1] > macd['MACD_Signal'][-1]:
                buy.append(ticker)
            elif macd['MACD'][-1] > macd['MACD_Signal'][-1]:
                sell.append(ticker)
            else:
                hold.append(ticker)
            
        return {
            'buy': buy,
            'sell': sell,
            'hold': hold
        }
        