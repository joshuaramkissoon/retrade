import datetime
from helpers.date_formatter import DateFormatter
from constants import USPH

class DateHelper:
    def __init__(self):
        self.us_public_holidays = USPH.data
        self.date_formatter = DateFormatter()

    def is_public_holiday(self, date):
        year = self.date_formatter.date_to_string(date, '%Y')
        date_str = self.date_formatter.date_to_string(date, '%B %d')
        if year in self.us_public_holidays:
            holiday_dates = self.us_public_holidays[year].values()
            return date_str in holiday_dates
        else:
            return False

    def is_weekend(self, date):
        return date.weekday() >= 5

    def is_market_open(self, date):
        return not self.is_public_holiday(date) and not self.is_weekend(date)

    def previous_day(self, date):
        return date + datetime.timedelta(days=-1)

    def next_day(self, date):
        return date + datetime.timedelta(days=1)

    def get_previous_open_day(self, date_string=None, date=None):
        if date_string:
            dt = self.date_formatter.string_to_date(date_string, '%d-%m-%Y') + datetime.timedelta(days=-1)
        if date:
            dt = date + datetime.timedelta(days=-1)
        while not self.is_market_open(dt):
            dt = self.previous_day(dt)
        return dt