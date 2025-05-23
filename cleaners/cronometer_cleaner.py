import pandas as pd

from utils import COL_DATETIME


def load_csv(file_path):
    return pd.read_csv(file_path)

def save_csv(df, file_path):
    df.to_csv(file_path, index=False)

def clean_csv(input_file, output_file):
    df = load_csv(input_file)

    df['Time'] = df['Time'].fillna('00:00 AM')  # Default time
    df[COL_DATETIME] = df['Day'].astype(str) + ' ' + df['Time'].astype(str)
    df[COL_DATETIME] = pd.to_datetime(df[COL_DATETIME])


    print(df[['Day', 'Time', COL_DATETIME]].head().to_markdown(index=False, numalign="left", stralign="left"))
    print(df.info())

    save_csv(df, output_file)
    print(f"Cleaned CSV saved to {output_file}")