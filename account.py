from algorithms import tradingstrategy, macd, mfi
from portfolio import Portfolio
import utility
from datetime import datetime

strategies = {
    'mfi' : mfi.MFI,
    'macd' : macd.MACD
}


class Account:
    def __init__(self, username, password, preinit = {}):
        self.username = username
        self.password = password
        self.portfolios = []
        if len(preinit) != 0:
            self._id = preinit['_id']
            for portfolio in preinit['portfolios']:
                strat = strategies[portfolio['strategy']['name']](portfolio['strategy'])
                self.portfolios.append(Portfolio(strat, portfolio['symbols'], portfolio['name']))


    def get_portfolios(self):
        return self.portfolios

    def add_portfolio(self, strategy, symbols=[], name="New Portfolio " + str(datetime.now())):
        self.portfolios.append(Portfolio(strategy, symbols, name))

    def get_total_earnings(self):
        earnings = 0
        for portfolio in self.portfolios:
            earnings += portfolio.get_earnings()
        return earnings

    

    def get_username(self):
        return self.username

    def reprJSON(self):
        return self.__dict__