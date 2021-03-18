import time
import datetime
from network.network import get
from helpers import DateFormatter, DateHelper
from constants import DateFormat

class Pricer:
    def __init__(self):
        self.secret_key_1 = 'c48c5bc486be4167a4ac2423e51ad277'
        self.secret_key_2 = 'add0d1a8efb04429a896cfc1d71f1091'
        self.secret_key = self.secret_key_1
        self.price_base_url = 'https://api.twelvedata.com/price'
        self.ts_base_url = 'https://api.twelvedata.com/time_series'
        self.stock_list_url = 'https://api.twelvedata.com/symbol_search'
        self.date_formatter = DateFormatter(DateFormat.ymd_short)

    def get_daily_price(self, stocks, date):
        '''
        Returns the open and close price of the specified stocks on the given date.
        Parameters:
        stock - A list of stock tickers
        date - A date object (date to get daily return on)
        '''
        print('Getting prices for %d stocks' % len(stocks))
        start = DateHelper.get_previous_open_day(date=date)
        start_str = self.date_formatter.date_to_string(start)
        end_str = self.date_formatter.date_to_string(date + datetime.timedelta(days=1))
        results = self.batch_handler(stocks, start=start_str, end=end_str) # Day change value for each stock
        return results

    def calculate_change(self, portfolio, dc_dict, is_local):
        '''
        Returns daily change and close value
        '''
        change = 0
        prev_close = 0
        curr_close = 0
        if is_local:
            for stock in dc_dict:
                prev_close += portfolio.get_asset_amount(stock)*dc_dict[stock][0]
                curr_close += portfolio.get_asset_amount(stock)*dc_dict[stock][1]
            change = curr_close - prev_close
        else:
            for stock in dc_dict:
                prev_close += portfolio[stock]*dc_dict[stock][0]
                curr_close += portfolio[stock]*dc_dict[stock][1]
            change = curr_close - prev_close
        return {'change': round(change, 2), 'prev_close': prev_close, 'curr_close': curr_close}
        

    def batch_handler(self, stocks, start, end, batch_size=8, sleep_time=60):
        '''
        Sends batch requests to API
        Gets price data on day of interest and previous day to compare the close on both days
        Limits to free plan is 12 requests per minute
        Returns:
        Dictionary of Stock Ticker: (Prev day close, Current day close)
        '''
        results = {} # Key: Stock ticker, Value: (Close price on previous day, Close price on current day)
        if len(stocks) <= batch_size:
            iters = 1
        else:
            iters = (len(stocks) // batch_size) if len(stocks)%batch_size == 0 else (len(stocks) // batch_size) + 1
        for i in range(iters):
            batch = stocks[i*batch_size:(i+1)*batch_size]
            stock_symbols = ','.join(batch)
            url = self.__make_url(stock_tickers=stock_symbols, start_date_str=start, end_date_str=end)
            res = get(url)
            prev_close = None
            curr_close = None
            if len(batch) < 2:
                if 'values' in res:
                    if len(res['values']) > 1:
                        # Valid values for both days
                        for day in res['values']:
                            if day['datetime'] == start:
                                prev_close = float(day['close'])
                            else:
                                curr_close = float(day['close'])
                        # change = curr_close - prev_close
                        results[batch[0]] = (prev_close, curr_close)
            else:
                for stock in res:
                    if 'values' in res[stock]:
                        if len(res[stock]['values']) > 1:
                            # Multiple stock request
                            for day in res[stock]['values']:
                                if day['datetime'] == start:
                                    prev_close = float(day['close'])
                                else:
                                    curr_close = float(day['close'])
                            # change = curr_close - prev_close
                            results[stock] = (prev_close, curr_close)
            if i != iters-1:
                # Wait 1 minute
                time.sleep(60)
        return results
        

    def __make_url(self, stock_tickers, start_date_str, end_date_str):
        '''
        Makes URL for API call depending on query type
        '''
        return self.ts_base_url + '?symbol=' + stock_tickers + '&start_date=' + start_date_str + '&end_date=' + end_date_str + '&interval=1day' + '&apikey=' + self.secret_key