from enum import Enum

class OrderColumn(Enum):
    action = 'Action'
    date = 'Time'
    ticker = 'Ticker'
    num_shares = 'No. of shares'

class OrderAction(Enum):
    buy = 'Buy'
    sell = 'Sell'

class DateFormat(Enum):
    ymd_short = '%Y-%m-%d'
    ymd_long = '%Y-%m-%d %H:%M:%S'

class USPublicHoliday(Enum):
    new_years_day = 'New Years Day'
    mlkj_day = 'Martin Luther King, Jr. Day'
    washington_day = "Washington's Birthday"
    good_friday = 'Good Friday'
    memorial_day = 'Memorial Day'
    independence_day = 'Independence Day'
    labor_day = 'Labor Day'
    thanksgiving = 'Thanksgiving Day'
    christmas = 'Christmas Day'

class USPH:
    usph = USPublicHoliday
    data = {
        '2020': {
            usph.new_years_day: 'January 01',
            usph.mlkj_day: 'January 20',
            usph.washington_day: 'February 17',
            usph.good_friday: 'April 10',
            usph.memorial_day: 'May 25',
            usph.independence_day: 'July 03',
            usph.labor_day: 'September 07',
            usph.thanksgiving: 'November 26',
            usph.christmas: 'December 25'
        },
        '2021': {
            usph.new_years_day: 'January 01',
            usph.mlkj_day: 'January 18',
            usph.washington_day: 'February 15',
            usph.good_friday: 'April 02',
            usph.memorial_day: 'May 31',
            usph.independence_day: 'July 05',
            usph.labor_day: 'September 06',
            usph.thanksgiving: 'November 25',
            usph.christmas: 'December 24'
        },
        '2022': {
            usph.new_years_day: None,
            usph.mlkj_day: 'January 18',
            usph.washington_day: 'February 15',
            usph.good_friday: 'April 02',
            usph.memorial_day: 'May 31',
            usph.independence_day: 'July 05',
            usph.labor_day: 'September 06',
            usph.thanksgiving: 'November 25',
            usph.christmas: 'December 24'
        }
    }

class StockFundamentals(Enum):
    industry = 'industry'
    sector = 'sector'

class PortfolioFilter(Enum):
    industry = 'industry'
    sector = 'sector'