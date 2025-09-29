import pandas as pd
import xlsxwriter,openpyxl
import os

import sys
def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Xcel():

    def __init__(self,user,name):
        self.input = user
        self.work_book = xlsxwriter.Workbook(get_path(name))

        self.work_sheet = self.work_book.add_worksheet("sheet")
        self.work_sheet.write(0, 0, "Category")
        self.work_sheet.write(0, 1, "Question")
        self.work_sheet.write(0, 2, "Answer")
        self.work_sheet.write(0, 3, "Insight")


        for index,entry in enumerate(self.input):

            self.work_sheet.write(index + 1, 0, str(entry["T"]))
            self.work_sheet.write(index + 1, 1, str(entry["Q"]))
            self.work_sheet.write(index + 1, 2, str(entry["A"]))
            self.work_sheet.write(index + 1, 3, str(entry["I"]))

        self.work_book.close()



    def combine_excel_files(self):
        df = [pd.read_excel(get_path(os.path.join('excel', file))) for file in os.listdir(get_path('excel')) if
              file.endswith('.xlsx')]
        if df:
            combined_df = pd.concat(df, ignore_index=True)
            combined_df.insert(0, 'Index', range(1, len(combined_df) + 1))
            combined_df.to_excel(get_path('final.xlsx'), index=False)


