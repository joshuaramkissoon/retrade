import yfinance as yf
from constants import StockFundamentals

class AssetFundamentals:
    
    def get_fundamentals(stock_ticker):
        ticker = yf.Ticker(stock_ticker)
        try:
            info = ticker.info
            return info
        except Exception as e:
            raise Exception(e)

    def get_industry(stock_ticker):
        try:
            info = AssetFundamentals.get_fundamentals(stock_ticker)
            return info.get('industry')
        except Exception as e:
            raise Exception(e)

    def get_stock_fundamental(fundamental, stocks):
        s = ' '.join(stocks)
        tickers = yf.Tickers(s)
        res = {} # {Fundamental: [Stocks]}
        for ticker in tickers.tickers:
            try:
                asset_class = ticker.info.get('quoteType')
                if asset_class != 'EQUITY':
                    print('%s is not an equity asset, it is a %s.' % (ticker.ticker, asset_class))
                    continue
                fnd = ticker.info.get(fundamental.value)
                if fnd not in res:
                    res[fnd] = [ticker.ticker]
                else:
                    res[fnd].append(ticker.ticker)
            except:
                print('No fundamentals for ticker: ', ticker.ticker)
                continue
        return res      


    def get_sector(stock_ticker):
        try:
            info = AssetFundamentals.get_fundamentals(stock_ticker)
            return info.get('sector')
        except Exception as e:
            raise Exception(e)
