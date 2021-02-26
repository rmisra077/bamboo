import alpaca_trade_api as tradeapi

# ALPACA Live Trading Info

# Client ID: PK42V8WYPH6UO0W2VEYU

# Client Secret: 81bcd34236e3da1000db1fac7703faae8a13edfd
# ----------
# ALPACA Paper Trading Info

# App ID: PK42V8WYPH6UO0W2VEYU

# Secret Key: vZHd5tb55JBjTiuptbgV6T6SNPxFD0UTXUSArXU2

api = tradeapi.REST('PK42V8WYPH6UO0W2VEYU', 'vZHd5tb55JBjTiuptbgV6T6SNPxFD0UTXUSArXU2', base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below
account = api.get_account()

# api.list_positions()
# api.get_account()

def get_holdings():
    """
    Gets list of tickers in user's portfolio
    """
    return [x.symbol for x in api.list_positions()]

def get_account():
    """
    Gets user's Alpaca account details
    """
    return api.get_account()

def place_trade(symbol, qty, buysell):
    """
    Places a trade using Alpaca
    """
    api.submit_order(
        symbol=symbol,
        side=buysell,
        qty=qty,
        type='market',
        time_in_force='gtc'
    )