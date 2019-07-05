import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Sheets():
    def __init__(self, sheet_name: str, json_file: str):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, self.scope)
        self.client = gspread.authorize(self.creds)

        self.sheet = self.client.open(sheet_name).sheet1

    def get_row(self, row_number):
        return self.sheet.row_values(row_number)

    def get_col(self, row_number):
        return self.sheet.col_values(row_number)
