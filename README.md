# Lab2
# Overview
This project allows you to import data from a CSV file into Google Sheets and export data from Google Sheets back to a CSV file using the Google Sheets API and the gspread library. It also features logging to track operations and errors and all is automated by github actions with help of ci.yml file.

- import_csv_to_sheet.py: Contains functions to import data from a CSV file to Google Sheets.
- export_sheet_to_csv.py: Contains functions to export data from a Google Sheets to CSV file.
- clean_and_standardize_data: Cleans data that has missing values and standardize it. After everything is done it generates report about all things done. 
