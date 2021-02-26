import algorithms
from datetime import datetime
import livetrading

class Portfolio:
    def __init__(self, strategy, symbols, name):
        self.name = name
        self.value = 0
        self.earnings = 0
        self.symbols = symbols #List of stock ticker symbols in the portfolio
        self.strategy = strategy

    def get_symbols(self):
        return self.symbols

    def get_holdings(self):
        return livetrading.get_holdings()
    
    def get_value(self):
        return self.value
    
    def get_earnings(self):
        return self.earnings

    def update(self):
        signals = self.strategy.get_signals(self.symbols)
        print(signals)

    def add_symbols(self, symbols):
        self.symbols.extend(symbols)
        self.symbols = list(set(self.symbols))
    
    def change_name(self, name):
        self.name = name

    def get_name(self):
        return self.name


    def reprJSON(self):
        return self.__dict__