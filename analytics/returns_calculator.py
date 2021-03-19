from assets import Pricer

class ReturnsCalculator:
    def __init__(self, is_local):
        self.is_local = is_local

    def get_daily_change(self, portfolio, date):
        '''
        Gets daily change for a portfolio on a given date.

        Parameters
        ----------
        portfolio: dict - {stock: amount}
        date: datetime object

        Returns
        -------
        dict - containing amt_change, percent_change, today_close
        '''
        if self.is_local:
            stock_change_dict = Pricer.get_daily_price(portfolio.get_assets(), date)
            daily_info_dict = Pricer.calculate_change(portfolio, stock_change_dict, is_local=self.is_local)
            percent_change = daily_info_dict['change']*100/daily_info_dict['prev_close'] # Daily change is (Close - Prev. Day Close)/Prev. Day Close
            return daily_info_dict['change'], percent_change, daily_info_dict['curr_close']
        else:
            stock_change_dict = Pricer.get_daily_price(list(portfolio.keys()), date)
            daily_info_dict = Pricer.calculate_change(portfolio, stock_change_dict, is_local=self.is_local)
            percent_change = daily_info_dict['change']*100/daily_info_dict['prev_close'] # Daily change is (Close - Prev. Day Close)/Prev. Day Close
            daily_info_dict['percent_change'] = percent_change
            return daily_info_dict