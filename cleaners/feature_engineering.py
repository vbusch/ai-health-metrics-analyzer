import datetime

import pandas as pd

from utils import COL_FOOD_NAME, COL_DAIRY, COL_SINCE_LAST_DAIRY, COL_SUGAR, COL_DATE, COL_DATETIME, \
    COL_DAIRY_LAST_CONSUMED_DAYS, get_time_of_day, COL_HEART_RATE, COL_HR_ROLLING_1H_AVG, COL_HR_ROLLING_3H_AVG


def augmented_data_features(df_merged):
    df_merged[COL_DATE] = df_merged[COL_DATETIME].dt.date

    #Dairy
    df_merged[COL_DAIRY] = df_merged[COL_FOOD_NAME].apply(is_dairy)
    dairy_per_day = df_merged.groupby(COL_DATE)[COL_DAIRY].max().reset_index()
    dairy_per_day[COL_DAIRY_LAST_CONSUMED_DAYS] = dairy_per_day[COL_DAIRY].rolling(window=3, min_periods=1).sum()
    df_merged[COL_SINCE_LAST_DAIRY] = calculate_days_since_last_dairy(df_merged)

    df_merged[COL_DATE] = df_merged[COL_DATETIME].dt.date
    df_merged = df_merged.merge(dairy_per_day[[COL_DATE, COL_DAIRY_LAST_CONSUMED_DAYS]], on=COL_DATE, how='left')

    # SUGAR
    sugar_per_day = df_merged.groupby(COL_DATE)[COL_SUGAR].sum().reset_index()
    df_merged = df_merged.merge(sugar_per_day[[COL_DATE, COL_SUGAR]], on=COL_DATE, how='left',
                                suffixes=('', '_day_total'))
    df_merged['total_sugar_consumed_today'] = df_merged[COL_SUGAR+'_day_total'].fillna(0)


    df_merged['hour'] = df_merged[COL_DATETIME].dt.hour
    df_merged['time_of_day'] = df_merged['hour'].apply(get_time_of_day)
    df_merged = pd.get_dummies(df_merged, columns=['time_of_day'], prefix='time')

    df_merged[COL_HR_ROLLING_1H_AVG] = df_merged.rolling(window='1H', on=COL_DATETIME)[COL_HEART_RATE].mean()
    df_merged[COL_HR_ROLLING_3H_AVG] = df_merged.rolling(window='3H', on=COL_DATETIME)[COL_HEART_RATE].mean()

    print(df_merged.columns)
    print(f"COLUMNS {df_merged.dtypes}")
    return df_merged


def merge_data(df_food, df_garmin):

    df_merged = pd.merge_asof(df_food, df_garmin, left_on=COL_DATETIME, right_on='timestamp', direction='nearest',
                              tolerance=pd.Timedelta('1 hour'))
    df_merged = df_merged.fillna(0)
    print(df_merged)

    print("\nMerged DataFrame (first 10 rows):")
    print(df_merged.head(10).to_markdown(index=False, numalign="left", stralign="left"))
    print("\nMerged DataFrame Info:")
    print(df_merged.info())
    return df_merged


def calculate_days_since_last_dairy(df):

    last_dairy_date = datetime.date(2025, 5, 5)  # Initialize to a very early date
    days_since = []

    for current_date in df[COL_DATE]:
        if df.loc[df[COL_DATE] == current_date, COL_DAIRY].max() == 1:
            days_since_last = (current_date - last_dairy_date).days
            last_dairy_date = current_date
        else:
            days_since_last = (current_date - last_dairy_date).days
        days_since.append(days_since_last)

    return days_since

def is_dairy(food_name):
    if not isinstance(food_name, str):
        return 0  # Not a string, assume not dairy

    food_name_lower = food_name.lower()

    dairy_words = ["milk", "cheese", "yogurt", "butter", "cream", "whey", "casein", "lactose"]
    non_dairy_words = ["vegan", "dairy-free"]

    exclusions = ["kirkland signature, mixed nut butter, with seeds", "peanut butter"]

    if food_name_lower in exclusions:
        return 0

    for word in non_dairy_words:
        if word in food_name_lower:
            return 0

    for word in dairy_words:
        if word in food_name_lower:
            return 1

    return 0  # Default: not dairy
