import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import pandas_datareader.data as web
import json



# Alpha Vantage API Key: 5W3J6GN17RFRE3A0
avkey = '5W3J6GN17RFRE3A0'



def get_ticker_price(ticker, date=False):
    """
    Gets the current stock price for the specified ticker, and returns that optionally with the current GMT time 
    """
    url = 'https://finance.yahoo.com/quote/'+ticker
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if date:
        return (soup.find_all(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].get_text(), time.asctime(time.gmtime()))
    else:
        return soup.find_all(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].get_text()

def live_lookup_avg():
    """
    Gets the average lookup time to get live stock price data based on 10 S&P500 stock lookup times
    """
    sp = sp500()
    times = []
    for ticker in sp[:10]:
        start = time.time()
        price = get_ticker_price(ticker)
        end = time.time()
        times.append(end-start)
    
    return sum(times)/len(times)

def sp500():
    """
    Gets tickers of companies in S&P500
    """
    df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    return list(df['Symbol'].unique())

def djia():
    """
    Gets tickers of companies in Dow Jones Industrial Average
    """
    df = pd.read_html('https://finance.yahoo.com/quote/%5EDJI/components/')[0]
    return list(df['Symbol'].unique())

def get_options_chart(ticker, option_type):
    """
    Returns either calls or puts options chart for ticker
    """
    url = 'https://finance.yahoo.com/quote/' + ticker + '/options'
    data = pd.read_html(url)
    if option_type == 'calls':
        return data[0]
    elif option_type == 'puts':
        return data[1]
    else:
        raise ValueError('Must input calls or puts')

def av_call(function, parameters={}):
    """
    Returns the result of a call to the Alpha Vantage API for the given function with the given parameters
    """
    url = 'https://www.alphavantage.co/query?function='+function
    for param in parameters.keys():
        url += '&' + param + '=' + parameters[param]
    url += '&apikey='+avkey
    data = requests.get(url)
    return data.json()

def get_daily_data_df(ticker, start, end):
    """
    Uses pandas_datareader library to return a DataFrame for daily stock data for a particular ticker from Yahoo API
    """

    return web.DataReader(ticker, "yahoo", start, end)

def get_df_from_av_json(json_obj):
    """
    Returns a date-indexed, chronologically forward dataframe of the JSON data returned by a call to the AlphaVantage API
    """
    print(json_obj)
    df = pd.DataFrame(list(json_obj.items())[1][1]).T.reset_index().iloc[::-1]
    df['index'] = pd.to_datetime(df['index'])
    df = df.set_index('index')
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])
    return df

class ComplexEncoder(json.JSONEncoder):
    """
    Class used to help with serialization of Account objects (method below)
    """
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

def serialize_account(acc):
    """
    Serializes account object to String JSON format to be put into MongoDB database
    """
    # account = acc.__dict__
    # portfoliolist = []
    # for portfolio in account['portfolios']:
    #     updated = portfolio.__dict__
    #     updated['strategy'] = updated['strategy'].__dict__
    #     portfoliolist.append(updated)
    #     account['portfolios'].remove(portfolio)
    # account['portfolios'] = portfoliolist
    return json.loads(json.dumps(acc.reprJSON(), cls=ComplexEncoder))

def deserialize_account(acc_json):
    """
    Deserializes JSON for an account and returns an Account object
    """
    pass