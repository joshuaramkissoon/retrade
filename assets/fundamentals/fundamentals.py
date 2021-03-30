import yfinance as yf
from constants import StockFundamentals, StockGrouping

class AssetFundamentals:
    
    def get_all_fundamentals(stock_ticker):
        ticker = yf.Ticker(stock_ticker)
        try:
            info = ticker.info
            return info
        except Exception as e:
            raise Exception(e)

    def get_industry(stock_ticker):
        try:
            info = AssetFundamentals.get_all_fundamentals(stock_ticker)
            return info.get('industry')
        except Exception as e:
            raise Exception(e)

    def get_stocks_by_group(group: StockGrouping, stocks):
        '''
        Groups a list of stocks by certain grouping criteria.
        Parameters
        ----------
        group (StockGrouping enum) - how to group stocks
        stocks - list of stock tickers (str)

        Returns
        -------
        dict - Dictionary {group: [stocks]}
        '''
        s = ' '.join(stocks)
        tickers = yf.Tickers(s)
        res = {} # {Group: [Stocks]}
        for ticker in tickers.tickers:
            try:
                if (asset_class := ticker.info.get('quoteType')) != 'EQUITY':
                    print('%s is not an equity asset, it is a %s.' % (ticker.ticker, asset_class))
                    continue
                if (grp := ticker.info.get(group.value)) not in res:
                    res[grp] = [ticker.ticker]
                else:
                    res[grp].append(ticker.ticker)
            except:
                print('No grouping for ticker: ', ticker.ticker)
        return res    

    def get_fundamental(fundamental: StockFundamentals, stocks):
        '''
        Gets specified fundamental for a list of stocks.
        Parameters
        ----------
        fundamental (StockFundamental) - fundamental to get for each stock
        stocks (list of str) - stock tickers to get fundamentals for

        Returns
        -------
        dict - {stock: fundamental}
        '''
        s = ' '.join(stocks)
        tickers = yf.Tickers(s)
        res = {}
        for ticker in tickers.tickers:
            try:
                if fnd := ticker.info.get(fundamental.value):
                    if ticker not in res:
                        res[ticker.ticker] = fnd
                else:
                    print('No %s for ticker: %s ' % (fundamental.value, ticker.ticker))    
                    continue
            except:
                print('No %s for ticker: %s ' % (fundamental.value, ticker.ticker))
        return res


    def get_sector(stock_ticker):
        try:
            info = AssetFundamentals.get_all_fundamentals(stock_ticker)
            return info.get('sector')
        except Exception as e:
            raise Exception(e)
