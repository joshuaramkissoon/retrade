from data import DataLoader, OrderParser
from helpers import DateFormatter, DateHelper
from constants import DateFormat, OrderColumn
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


    