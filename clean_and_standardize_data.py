import pandas as pd
import numpy as np
import logging

logging.basicConfig(
    filename='log.txt',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

total_rows = 0
rows_deleted = 0
rows_changed = 0


def clean_data(path):
    global total_rows, rows_deleted, rows_changed

    df = pd.read_csv('output_data.csv')
    logging.info("Data read from csv file.")

    total_rows = len(df)
    logging.info(f"Number of rows before cleaning phase: {total_rows}")

    rows_deleted = df[df.isnull().sum(axis=1) >= 3].shape[0]
    df = df.dropna(thresh=len(df.columns) - 2)

    logging.info(f"Number of rows deleted: {rows_deleted}")

    for i in df.columns:
        if df[i].isnull().sum() > 0:
            if df[i].dtype in [np.int64, np.float64]:
                median = df[i].median()
                missing = df[i].isnull().sum()
                df[i].fillna(median, inplace=True)
                if missing > 0:
                    rows_changed += missing
            else:
                most_popular_value = df[i].mode()[0]
                missing = df[i].isnull().sum()
                df[i].fillna(most_popular_value, inplace=True)
                if missing > 0:
                    rows_changed += missing

    return df


def standardize_data(df):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df[num_cols] = (df[num_cols] - df[num_cols].mean()) / df[num_cols].std()

    logging.info("Data standardized")

    return df


def generate_report():
    total_deleted_percentage = (rows_deleted / total_rows * 100) if total_rows > 0 else 0
    total_changed_percentage = (rows_changed / total_rows * 100) if total_rows > 0 else 0

    report = f"""
    Report:

    Total number of Rows: {total_rows}
    Deleted rows: {rows_deleted} ({total_deleted_percentage:.2f}%)
    Changed rows: {rows_changed} ({total_changed_percentage:.2f}%)
    """

    with open('report.txt', 'w') as f:
        f.write(report)

    logging.info("Report saved to file: 'report.txt'.")

    print(report)


path = 'output_data.csv'

logging.info("Start cleaning phase")
df_clean = clean_data(path)
logging.info("End cleaning phase")

logging.info("Start standardize phase")
df_standardize = standardize_data(df_clean)
logging.info("End standardize phase")

df_standardize.to_csv('clean_data.csv', index=False)
logging.info("Data saved to file: clean_data.csv")

generate_report()
logging.info("End of preparing data")