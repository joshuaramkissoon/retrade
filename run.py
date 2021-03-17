from data import DataLoader, OrderParser
from analytics import ReturnsCalculator
from constants import OrderColumn
import datetime

path = 'order history Nov_Mar17.csv'
cols = [OrderColumn.date, OrderColumn.action, OrderColumn.ticker, OrderColumn.num_shares]
parser = OrderParser(DataLoader.load_order_csv(path, cols))
pf = parser.get_portfolio_on_date(datetime.datetime.now() + datetime.timedelta(days=-131))
print(ReturnsCalculator.get_daily_change(pf, datetime.datetime.now() + datetime.timedelta(days=-131)))
