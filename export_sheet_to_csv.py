import gspread
from google.oauth2.service_account import Credentials
import csv
import os
import json
import logging

logging.basicConfig(
    filename='log.txt',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def export_google_sheets_to_csv(csv_file_path):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    sheet_id = os.getenv('SHEET_ID')

    with open('credentials.json') as f:
        account_json = json.load(f)

    creds = Credentials.from_service_account_info(account_json, scopes=scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(sheet_id)
    sheet = spreadsheet.sheet1

    data = sheet.get_all_values()

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    logging.info(f"Data from the sheet has been saved to: {output_csv}.")


output_csv = 'output_data.csv'
export_google_sheets_to_csv(output_csv)
