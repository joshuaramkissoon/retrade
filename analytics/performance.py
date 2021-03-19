import numpy as np
from assets import Pricer

class PerformanceCalculator:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def industry_performance(self, industry, period='1mo', interval='30m'):
        # Get stocks in industry
        stocks = self.portfolio.get_stocks_in_industry(industry)
        # Get total value of industry
        industry_val, stock_amounts = self.portfolio.get_industry_value(industry)
        # Get weight of each stock in industry
        weights = {stock: stock_amounts[stock]/industry_val for stock in stock_amounts}
        print(weights)
        # Get price data for each stock
        price_data = Pricer.historic_data(stocks, period=period, interval=interval)
        if len(weights) == 0:
            raise Exception('No stocks in specified industry: %s' % industry)
        if len(weights) == 1:
            return price_data['Close'].tolist()
        # Combine price data using respective weights
        weighted_price = np.zeros((len(price_data.index)))
        for stock in weights:
            weighted_price += weights[stock]*np.array(price_data[stock]['Close'].tolist())
        return weighted_price