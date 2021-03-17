import datetime

class DateFormatter:
    def __init__(self, format=None):
        if format:
            self.format = format
    def string_to_date(self, s, format=None):
        if not format and not self.format:
            raise Exception('No format specified')
        if not format:
            return datetime.datetime.strptime(s, self.format.value)    
        return datetime.datetime.strptime(s, format)

    def date_to_string(self, d, format=None):
        if not format and not self.format:
            raise Exception('No format specified')
        if not format:
            return d.strftime(self.format.value)    
        return d.strftime(format)

    def string_to_string(self, s, original_format, target_format):
        '''
        Converts string to date object and then back to string in target format
        '''
        date = self.string_to_date(s, original_format.value)
        return self.date_to_string(date, format=target_format.value)