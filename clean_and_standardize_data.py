import pandas as pd
import numpy as np

total_rows = 0
rows_removed = 0
rows_modified = 0


def clean_data(path):
    global total_rows, rows_removed, rows_modified

    df = pd.read_csv('output_data.csv')

    total_rows = len(df)

    rows_removed = df[df.isnull().sum() >= 3].shape[0]
    df = df.dropna(thresh=len(df.columns) - 2)

    for i in df.columns:
        if df[i].isnull().sum() > 0:
            if df[i].dtype in [np.int64, np.float64]:
                median = df[i].median()
                missing = df[i].isnull().sum()
                df[i].fillna(median, inplace=True)
                if missing > 0:
                    rows_modified += missing
            else:
                most_popular_value = df[i].mode()[0]
                missing = df[i].isnull().sum()
                df[i].fillna(most_popular_value, inplace=True)
                if missing > 0:
                    rows_modified += missing

    return df


def standardize_data(df):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df[num_cols] = (df[num_cols] - df[num_cols].mean()) / df[num_cols].std()

    return df


path = 'output_data.csv'
df_clean = clean_data(path)
df_standardize = standardize_data(df_clean)

df_standardize.to_csv('clean_data.csv', index=False)
