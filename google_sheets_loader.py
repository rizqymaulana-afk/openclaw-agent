# google_sheets_loader.py

import gspread
import pandas as pd
import streamlit as st

from oauth2client.service_account import (
    ServiceAccountCredentials
)


class GoogleSheetsLoader:

    def __init__(self):

        # =========================
        # GOOGLE API SCOPE
        # =========================

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        # =========================
        # STREAMLIT SECRETS
        # =========================

        creds_dict = dict(
            st.secrets["gcp_service_account"]
        )

        # =========================
        # CREATE CREDENTIALS
        # =========================

        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict,
            scope
        )

        # =========================
        # AUTHORIZE CLIENT
        # =========================

        self.client = gspread.authorize(
            creds
        )

    # =========================
    # LOAD GOOGLE SHEET
    # =========================

    def load_sheet(
        self,
        spreadsheet_url,
        worksheet_name
    ):

        print(
            f"\nLoading spreadsheet: {spreadsheet_url}"
        )

        # =========================
        # OPEN SPREADSHEET
        # =========================

        spreadsheet = self.client.open_by_url(
            spreadsheet_url
        )

        # =========================
        # OPEN WORKSHEET
        # =========================

        worksheet = spreadsheet.worksheet(
            worksheet_name
        )

        # =========================
        # GET DATA
        # =========================

        records = worksheet.get_all_records()

        # =========================
        # CONVERT TO DATAFRAME
        # =========================

        df = pd.DataFrame(
            records
        )

        print(
            "\nSpreadsheet loaded!"
        )

        return df