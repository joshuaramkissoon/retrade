import pandas as pd
from data.data_handler import DataHandler

class DataLoader:
    def __init__(self):
        pass
    
    def load_order_csv(self, path, columns=None):
        # Load order csv data
        data = self.load_file(path, columns)
        # Parse columns
        dh = DataHandler()
        data = dh.format_csv_actions(data)
        dh.format_csv_dates(data)
        return data


    def load_file(self, path, columns=None):
        df = pd.read_csv(path)
        if columns:
            cols = [col.value for col in columns]
        if not columns:
            return df
        else:
            return df[cols]