import pandas as pd
from constants import OrderColumn, OrderAction, DateFormat
from helpers import DateFormatter

class OrderParser:
    '''
    Initialised with formatted order dataframe
    Formatting required a priori:
    - Dates in YYYY-MM-DD
    - Action can only be Buy or Sell
    '''
    
    def __init__(self, data):
        self.data = data
        self.MIN_THRESHOLD = 0.00001

    def get_portfolio_on_date(self, date):
        '''
        Gets all the open positions on given date
        1. Get all data from specified date to start date
        2. Loop through rows and populate dictionary of {stock: num_shares}, updating amount as necessary
        '''
        orders = self.get_orders_to_date(date)
        return self.get_asset_positions(orders)

    
    def get_orders_to_date(self, date):
        '''
        Returns a dataframe including all rows up to and including the date specified
        Arguments:
        date: date of interest (Date object)
        '''
        str_date = DateFormatter(DateFormat.ymd_short).date_to_string(date)
        filtered = self.data.loc[self.data[OrderColumn.date.value] <= str_date]
        if len(filtered) == 0:
            return None
        else: 
            return filtered

    def get_asset_positions(self, data):
        '''
        Return dictionary {stock: amount}
        '''
        if data is None or len(data) == 0:
            return None
        positions = {}
        for index, order in data.iterrows():
            stock = order[OrderColumn.ticker.value]
            action = order[OrderColumn.action.value]
            amount = order[OrderColumn.num_shares.value]
            if stock in positions:
                # Update stock amount
                if action == OrderAction.buy:
                    # Add amount to current amount
                    positions[stock] += amount
                elif action == OrderAction.sell:
                    # Subtract amount from current amount
                    if positions[stock] - amount < self.MIN_THRESHOLD:
                        # No longer holding stock
                        del positions[stock]
                    else:
                        positions[stock] -= amount
                    
            else:
                # Add stock to positions
                positions[stock] = amount if action == OrderAction.buy else -amount
        return positions
            

    