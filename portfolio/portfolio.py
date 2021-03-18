from data import DataLoader, OrderParser
from assets.fundamentals import AssetFundamentals
from assets.pricer import Pricer
from helpers import DateFormatter, DateHelper
from constants import DateFormat, OrderColumn, StockFundamentals, Industry
import datetime

class Portfolio:
    def __init__(self, positions=None, path=None, format_data=True):
        if positions:
            self.parser = None
            self.positions = positions
            return
        if path:
            # Load data from file
            cols = [OrderColumn.date, OrderColumn.action, OrderColumn.ticker, OrderColumn.num_shares] if format_data else None
            self.data = DataLoader.load_order_csv(path, cols)
            self.parser = OrderParser(self.data)
            self.positions = self.parser.get_portfolio_on_date(datetime.datetime.now())
    
    def get_stocks(self, date=None):
        '''
        Returns the stocks in a portfolio on a given date.

        Parameters
        -----------
        date: str (YYYY-mm-dd)

        Returns
        -------
        list: containing stock tickers
        '''
        try:
            return list(self.get_positions(date).keys())
        except Exception as e:
            raise Exception(e)
    
    def get_positions(self, date=None) -> dict:
        '''
        Returns the positions in a portfolio on a given date.

        Parameters
        -----------
        date: str (YYYY-mm-dd)

        Returns
        -------
        dict: containing positions {stock: amount}
        '''
        if not self.positions:
            raise Exception('No portfolio data loaded')
        if not date:
            return self.positions
        else:
            if not self.parser:
                raise Exception('Portfolio object initialised with position data. To get positions on any date, initialise the Portfolio object with a path to an Order History CSV file.')
            dt = DateFormatter(DateFormat.ymd_short).string_to_date(date)
            if DateHelper.is_future(dt):
                raise Exception('Date must be less than or equal to current date')
            return self.parser.get_portfolio_on_date(dt)


    def get_fundamentals(self, fundamental: StockFundamentals, date=None):
        '''
        Gets the specified fundamental for all positions in a portfolio on a given date.

        Parameters
        -----------
        date: str (YYYY-mm-dd)

        Returns
        -------
        dict: containing fundamentals {fundamental: list of stocks}
        '''
        try:
            return AssetFundamentals.get_stock_fundamental(fundamental, self.get_stocks(date))
        except Exception as e:
            raise Exception(e)

    def get_industry_allocations(self, date=None):
        '''
        position weight = total value of position / total value of portfolio
        '''
        # Categorise stocks by industry
        industry_dict = self.get_fundamentals(StockFundamentals.industry, date=date)
        # positions_dict = self.get_positions(date)
        # prices_dict = Pricer.get_current_price(positions_dict)
        self.total_val = self.get_total_value(date)
        res = {}
        for industry in industry_dict:
            stocks = industry_dict[industry]
            val = self.get_value(stocks, self.positions_dict, self.prices_dict)
            pct = val*100/self.total_val
            res[industry] = pct
        return res

    def get_value(self, stocks, positions, prices):
        '''
        Gets the total value of a list of stocks given a dictionary of positions for a portfolio
        '''
        val = 0
        for stock in stocks:
            val += positions[stock]*prices[stock]
        return val

    def get_stocks_in_industry(self, industry_data=None, industry: str=None, date=None):
        if not industry_data:
            industry_data = self.get_fundamentals(StockFundamentals.industry, date)
        return industry_data.get(industry)


    def get_total_value(self, date=None):
        '''
        Gets the total value of the portfolio.
        Note: Stocks that aren't supported by yfinance API won't be accounted for
        '''
        self.positions_dict = self.get_positions(date)
        self.prices_dict = Pricer.get_current_price(self.positions_dict)
        val = 0
        for stock in self.prices_dict:
            val += self.positions_dict[stock]*self.prices_dict[stock]
        return val
