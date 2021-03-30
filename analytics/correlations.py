from assets import Pricer

class CorrelationCalculator:

    def get_correlation(stock, ref_asset, period):
        ref_price_list = Pricer.get_price_history(ref_asset, period=period)
        stock_price_list = Pricer.get_price_history(stock, period=period)
        return ref_price_list, stock_price_list