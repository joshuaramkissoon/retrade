import numpy as np
import pandas as pd
from assets import Pricer, AssetFundamentals
from constants import StockGrouping, StockFundamentals
from analytics.metrics import standard_deviation
import matplotlib.pyplot as plt

class PerformanceCalculator:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def industry_performance(self, industry, period='1mo', interval='30m'):
        # Get stocks in industry
        stocks = self.portfolio.get_stocks_in_industry(industry)
        # Get total value of industry
        industry_val, stock_amounts = self.portfolio.get_industry_value(industry)
        # Get weight of each stock in industry
        weights = self.get_stock_weights(industry_val, stock_amounts)
        print(weights)
        # Get price data for each stock
        price_data = Pricer.historic_data(stocks, period=period, interval=interval)
        if not weights:
            raise Exception('No stocks in specified industry: %s' % industry)
        if len(weights) == 1:
            return price_data['Close'].tolist()
        # Combine price data using respective weights
        weighted_price = np.zeros((len(price_data.index)))
        for stock in weights:
            weighted_price += weights[stock]*np.array(price_data[stock]['Close'].tolist())
        return weighted_price

    def get_beta(self, group: StockGrouping=None):
        '''
        Gets beta for a portfolio or sub-group of a portfolio.
        '''
        total_val, stock_vals = self.portfolio.get_total_value()
        weights = self.get_stock_weights(total_val, stock_vals)
        beta_data = AssetFundamentals.get_fundamental(StockFundamentals.beta, stock_vals.keys())
        print(beta_data)
        
    def get_volatility(self):
        '''Gets volatility of assets in a portfolio.'''
        total_val, stock_vals = self.portfolio.get_total_value()
        weights = self.get_stock_weights(total_val, stock_vals)
        stocks = list(weights.keys())
        price_data = Pricer.historic_data(stocks, period='max', interval='1d')
        dct = self.get_volatility_dict(stocks, price_data)
        return sorted([(stock, dct[stock]) for stock in dct], key=lambda x: x[1], reverse=True)

    def get_volatility_dict(self, stocks, price_data) -> dict:
        '''Returns a dict {stock: std dev} given price data.'''
        if not stocks:
            raise Exception('No stocks specified')
        if len(stocks) == 1:
            return {stocks[0]: standard_deviation(self.get_returns_from_prices(stocks, price_data['Close']))}
        res = {stock: standard_deviation(self.get_returns_from_prices(stocks, price_data[stock]['Close'])) for stock in stocks}
        return res

    def get_returns_from_prices(self, stocks, price_data):
        if len(stocks) == 1:
            return price_data.diff()
        return price_data.dropna().diff().dropna()

    def get_stock_weights(self, total_value: float, stock_values: dict) -> dict:
        '''
        Calculates the weight of each stock in a group of stocks given the total value of the grouping.
        '''
        return {stock: stock_values[stock]/total_value for stock in stock_values}

class PerformanceSimulator:

    def __init__(self):
        pass

    def simulate(self, weights, period):
        '''
        Simulates price of asset pie for specified period.
        Parameters
        ----------
        weights (dict) - {stock: weight}
        period (str) - simulation period 

        Returns
        -------
        list - Price history
        '''
        price_data = Pricer.historic_data(weights.keys(), period=period, interval='1d')
        if len(weights) == 1:
            return price_data['Close']
        weighted_price = np.zeros((len(price_data.index)))
        for stock in weights:
            weighted_price += weights[stock]*np.array(price_data[stock]['Close'].tolist())
        ret = 100*(weighted_price[-1] - weighted_price[0])/weighted_price[0]
        plt.figure()
        plt.plot(weighted_price)

        for stock in weights:
            price = Pricer.historic_data([stock], period=period, interval='1d').reset_index(drop=True)
            plt.plot(price['Close'])
        
        plt.legend(['Combined'] + list(weights.keys()))
        plt.show()
        return weighted_price, ret
