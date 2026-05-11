# google_sheets_loader.py

import gspread

from oauth2client.service_account import (
    ServiceAccountCredentials
)

import pandas as pd


class GoogleSheetsLoader:

    def __init__(self):

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json",
            scope
        )

        self.client = gspread.authorize(
            creds
        )

    # =========================
    # LOAD GOOGLE SHEET
    # =========================

    def load_sheet(
        self,
        spreadsheet_name,
        worksheet_name
    ):

        print(
            f"\nLoading spreadsheet: {spreadsheet_name}"
        )

        sheet = self.client.open_by_url(
            spreadsheet_name
        )

        worksheet = sheet.worksheet(
            worksheet_name
        )

        data = worksheet.get_all_records()

        df = pd.DataFrame(
            data
        )

        print(
            "\nSpreadsheet loaded!"
        )

        return df