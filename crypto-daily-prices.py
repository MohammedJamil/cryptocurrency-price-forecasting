#!/usr/bin/env python
# coding: utf-8

# # Cryptocurrency Market Analysis
# 
# *Mohammed Jamil*

# ## Context
# 
# The first half of 2022 has been very bad for the crypto market. Crypto industry experts have mixed opinions about the future of cryptocurrencies. While some believe the market will continue to be volatile, others expect some stability in the second half of 2022.
# 
# In these uncertain times for the crypto market, is it still worth the risk investing in cryptocurrencies ? and what are the low-risk cryptocurrencies to consider ? These are some questions that we will try to answer in this exploratory analysis and the other notebooks included in this project.


import pandas as pd
import numpy as np
import requests
import datetime
import time



# To collect cryptocurrency market data, we are going to use the **CoinGecko** API.

def get_topN_currencies(n, vs_currency="usd"):
    """
    Retreives the top N cryptocurrencies with the highest market value (N_max = 250).
    
    Params:
    -------
        vs_currency (String) - The target currency of market data.
        n (Integer)          - Number of currencies.
    
    Returns:
    --------
        Top N currencies, their id and symbols (pandas.DataFrame).
    """
    
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": vs_currency, "order": "market_cap_desc", "per_page": n, "page": 1, "sparkline":False}
    response = requests.get(url, params=params)
    result = np.array(list(map(lambda x: [x['id'], x['symbol'], x['name'], x['market_cap'], x['total_volume']], response.json())))
    data = pd.DataFrame.from_dict({'id': result[:,0],
                                   'symbol': result[:,1],
                                   'name': result[:,2],
                                   'market_cap': result[:,3],
                                   'volume': result[:,4]})
    data = data.astype({"market_cap": float, "volume": float})
    
    return data


def coin_historical_prices(coin_id, vs_currency='usd', nb_days='max'):
    """
    Fetchs historical daily prices about a specific cryptocurrency from the CoinGecko's API.
    
    Params:
    -------
        coin_sym (String)    - Cryptocurrency id .
        vs_currency (String) - The target currency of market data.
        nb_days (Integer or "max") - Data up to number of days ago (1/7/14/30/90/180/365/max)
    
    Returns:
    --------
        Market historical daily prices of the specified cryptocurrency (pandas.DataFrame).
    
    """
    
    url = "https://api.coingecko.com/api/v3/coins/{}/market_chart".format(coin_id)
    params = {'vs_currency': vs_currency, 'days':nb_days}
    response = requests.get(url, params=params)
    result = np.array(response.json()["prices"])
    data = pd.DataFrame.from_dict({'date': result[:,0],
                                   'price': result[:,1]})
    data.date = data.date.apply(lambda x: datetime.date.fromtimestamp(x/1000))
    data = data.astype({"price": float})
    data.insert(0, "id", coin_id, True)
    
    return data 


# Retreiving the top 10 currencies ohlc data.

currencies_df = get_topN_currencies(10)
all_coin_prices_df = pd.concat([coin_historical_prices(id) for id in currencies_df['id'].head(10)])   

# Exporting dataframe as a csv file.

all_coin_prices_df.to_csv("top10-crypto-daily-prices.csv")