# -*- coding: utf-8 -*-
"""
@Time    : 2019-12-26 19:40
@Author  : jackie
"""

from xlrd import open_workbook


class MyXls:
    def __init__(self, file_path):
        self.file = open_workbook(file_path)
        self.sheet_names = self.file.sheet_names()

    def get_sheet(self, sheet_name):
        sheet = self.file.sheet_by_name(sheet_name)
        row_num = sheet.nrows

        sheet_data = {}

        for i in range(1, row_num):
            row_data = sheet.row_values(rowx=i)
            foreign_key = row_data[0]
            if foreign_key not in sheet_data.keys():
                sheet_data[foreign_key] = []
            data = {}
            for index, key in enumerate(sheet.row_values(0)):
                data[key] = row_data[index]
                data['host'] = sheet_name
            sheet_data[foreign_key].append(data)
        return sheet_data
