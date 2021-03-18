from analytics import ReturnsCalculator
from data import DataLoader, OrderParser
from constants import OrderColumn, StockFundamentals, PortfolioFilter
import datetime


path = 'order history Nov_Mar18.csv'
# cols = [OrderColumn.date, OrderColumn.action, OrderColumn.ticker, OrderColumn.num_shares]
# parser = OrderParser(DataLoader.load_order_csv(path, cols))
# d = parser.get_portfolio_on_date(datetime.datetime.now())
# print(ReturnsCalculator.get_daily_change(pf, datetime.datetime.now() + datetime.timedelta(days=-132)))


from portfolio import Portfolio
from visualisations.visualisations import plot_allocations

pf = Portfolio(path=path)
res = pf.get_group_allocations(PortfolioFilter.industry, include_stocks=False)
plot_allocations(PortfolioFilter.industry, res)


