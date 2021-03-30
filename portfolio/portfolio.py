from data import DataLoader, OrderParser
from assets.fundamentals import AssetFundamentals
from assets.pricer import Pricer
from helpers import DateFormatter, DateHelper
from constants import DateFormat, OrderColumn, StockFundamentals, StockGrouping, PortfolioFilter, PriceData
import datetime
from math import isnan

class Portfolio:
    def __init__(self, positions=None, path=None, format_data=True):
        self.industry_data = None
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

    def get_portfolio_weights(self, date=None):
        '''
        Returns the positions and weights for each position in a portfolio on a given date.

        Parameters
        -----------
        date: str (YYYY-mm-dd)

        Returns
        -------
        dict: containing positions {stock: weight}
        '''
        total_val, stock_vals = self.get_total_value(date)
        return {stock: stock_vals[stock]/total_val for stock in stock_vals}


    def get_stocks_by_group(self, group: StockGrouping, date=None):
        '''
        Group all stocks in a portfolio on a given date by criteria. Returns all stocks if group is None.

        Parameters
        -----------
        group: StockGrouping
        date: str (YYYY-mm-dd)

        Returns
        -------
        dict: containing fundamentals {group: list of stocks}
        '''
        try:
            return AssetFundamentals.get_stocks_by_group(group, self.get_stocks(date))
        except Exception as e:
            raise Exception(e)

    def get_group_allocations(self, group: StockGrouping, date=None, include_stocks=False):
        filter_dict = self.get_stocks_by_group(group, date=date)
        self.total_val, _ = self.get_total_value(date)
        res = {}
        for group in filter_dict:
            stocks = filter_dict[group]
            val = self.get_value(stocks, self.positions_dict, self.prices_dict)
            pct = val*100/self.total_val
            res[group] = (stocks, pct) if include_stocks else pct

        if include_stocks:
            sorted_res = sorted([(stock, res[stock][0], res[stock][1]) for stock in res], key=lambda x: x[2], reverse=True)
        else:
            sorted_res = sorted([(stock, res[stock]) for stock in res], key=lambda x: x[1], reverse=True)
        return sorted_res

    def get_value(self, stocks, positions, prices):
        '''
        Gets the total value of a list of stocks given a dictionary of positions for a portfolio
        '''
        val = 0
        for stock in stocks:
            val += positions[stock]*prices[stock]
        return val

    def get_stocks_in_industry(self, industry: str, industry_data=None, date=None):
        if not industry_data:
            self.industry_data = self.get_stocks_by_group(StockGrouping.industry, date)
            # print(self.industry_data)
        return self.industry_data.get(industry)


    def get_industry_value(self, industry: str, date=None):
        if not self.industry_data:
            stocks = self.get_stocks_in_industry(industry, date=date)
        else:
            stocks = self.industry_data.get(industry)
        if not stocks:
            raise Exception('No stocks in industry: %s' % industry)
        positions = self.get_positions(date)
        prices_dict = Pricer.get_current_price(positions)
        vals = {}
        industry_val = 0
        for stock in stocks:
            amount = positions[stock]*prices_dict[stock]
            industry_val += amount
            vals[stock] = amount
        return industry_val, vals
        
    
    def get_total_value(self, date=None):
        '''
        Gets the total value of the portfolio.
        Note: Stocks that aren't supported by yfinance API won't be accounted for
        '''
        self.positions_dict = self.get_positions(date)
        # TODO: Change price to price on specified date instead of current price
        self.prices_dict = Pricer.get_current_price(self.positions_dict)
        val = 0
        stock_vals = {}
        for stock in self.prices_dict:
            amt = self.positions_dict[stock]*self.prices_dict[stock]
            stock_vals[stock] = amt
            val += amt
        return val, stock_vals

    def summarise_performance(self, date:str=None):
        stocks = self.get_stocks(date)
        curr_date = DateFormatter(DateFormat.ymd_short).string_to_date(date)
        if not DateHelper.is_market_open(curr_date):
            raise Exception('Market not open on specified date: %s' % date)
        prev_date = DateFormatter(DateFormat.ymd_short).date_to_string(DateHelper.get_previous_open_day(date=curr_date))
        today_close = Pricer.get_price_on_date(stocks, date, PriceData.adj_close)
        prev_close = Pricer.get_price_on_date(stocks, prev_date, PriceData.adj_close)
        pct_change = {stock: (today_close[stock] - prev_close[stock])/prev_close[stock] for stock in today_close}
        pct_change = {k: pct_change[k] for k in pct_change if not isnan(pct_change[k])}
        sorted_change = sorted([(stock, 100*pct_change[stock]) for stock in pct_change], key=lambda x: x[1], reverse=True)
        for c in sorted_change:
            print('%s: %.2f' % (c[0], c[1]))