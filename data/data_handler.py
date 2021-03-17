import numpy as np
import pandas as pd
from constants import OrderAction, OrderColumn, DateFormat
from helpers import DateFormatter

class DataHandler:
    def __init__(self):
        pass


    def format_csv_actions(self, df):
        '''
        Changes all the action types to either Buy or Sell
        '''
        actions = np.array(df['Action'].unique())
        buy_types = np.where(['buy' in x for x in actions])[0]
        sell_types = np.where(['sell' in x for x in actions])[0]
        buy_types = actions[buy_types]
        sell_types = actions[sell_types]
        return df.replace(regex=buy_types, value=OrderAction.buy).replace(regex=sell_types, value=OrderAction.sell)

    def format_csv_dates(self, df):
        '''
        Converts the dates to YYYY-MM-DD
        '''
        column = OrderColumn.date
        df[column.value] = df[column.value].apply(lambda dt: DateFormatter().string_to_string(dt, original_format=DateFormat.ymd_long, target_format=DateFormat.ymd_short))

    def write_to_file(self, workbook, data, path):
        print(data)
        for i, row in enumerate(workbook.active.iter_rows(min_row=workbook.active.max_row+1, max_col=len(data[0]), max_row=workbook.active.max_row + len(data))):
            row[0].value = data[i]['date']
            row[1].value = data[i]['dca']
            row[2].value = data[i]['dcp']
            row[3].value = data[i]['close']
        workbook.save(path)

    def insert_row_data(self, workbook, row, data, path):
        '''
        Inserts a new row of data into the workbook's active sheet at index row 
        Parameters:
        row - Int (0 means insert new row before first row of data excluding headers)
        data - Dictionary containing date, dca, dcp and close values
        path - Path to save file to
        '''

        pyxl_row = row + 2
        workbook.active.insert_rows(pyxl_row)
        # Save data
        # print(data)
        for row in workbook.active.iter_rows(min_row=pyxl_row, max_row=pyxl_row):
            row[0].value = data['date']
            row[1].value = data['dca']
            row[2].value = data['dcp']
            row[3].value = data['close']
        workbook.save(path)

    def delete_rows(self, start_index, num_rows, workbook=None, sheet=None, path=None):
        '''
        Deletes rows in a worksheet and saves the file
        start_index: Index of row to start deleting from (First row corresponds to index 0)
        num_rows: Number of rows to delete
        '''
        if not workbook or not path:
            raise Exception('No workbook or path specified')
        if not sheet:
            sheet = workbook.active
        sheet.delete_rows(start_index+2, num_rows)
    
    def get_insert_index(self, arr, target):
        '''
        Returns the index that the row with target date needs to be inserted above to make the array sorted
        Parameters:
        arr - List of date objects
        target - Date object
        '''

        arr = np.array(arr)
        arr = np.sort(arr)
        arr = np.append(arr, target)
        args = arr.argsort()
        return np.where(args == len(arr) - 1)