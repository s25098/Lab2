import gspread
from google.oauth2.service_account import Credentials
import os
import json
import logging
import csv

logging.basicConfig(
    filename='log.txt',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def import_csv_to_google_sheets(csv_file_path):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    sheet_id = os.getenv('SHEET_ID')

    with open('credentials.json') as f:
        account_json = json.load(f)

    creds = Credentials.from_service_account_info(account_json, scopes=scope)
    client = gspread.authorize(creds)

    worksheet = client.open_by_key(sheet_id)
    sheet = worksheet.sheet1

    sheet.clear()
    logging.info("Google Sheet cleared.")

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)
        sheet.update(csv_data)

    logging.info(f"CSV {csv_file_path} has been imported to Google Sheets.")


csv_file = "data_student_25098.csv"

import_csv_to_google_sheets(csv_file)
