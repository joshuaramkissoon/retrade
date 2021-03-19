from analytics import ReturnsCalculator
from data import DataLoader, OrderParser
from constants import OrderColumn, StockFundamentals, PortfolioFilter
import datetime
from portfolio import Portfolio
from visualisations.visualisations import plot_allocations, line_plot
from analytics.performance import PerformanceCalculator


path = 'order history Nov_Mar18.csv'
pf = Portfolio(path=path)

industry = 'Software—Application'

p = PerformanceCalculator(pf).industry_performance(industry, period='6mo', interval='60m')
line_plot(p)