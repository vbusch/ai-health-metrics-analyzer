import datetime
import json
import os

import pandas as pd

COL_FOOD_NAME = 'Food Name'
COL_SUGAR_TODAY = 'total_sugar_consumed_today'
COL_SUGAR = 'Sugars (g)'
COL_DAIRY = 'dairy'
COL_SINCE_LAST_DAIRY = 'days_since_last_dairy'
COL_DAIRY_LAST_CONSUMED_DAYS = 'dairy_consumed_last_3_days'
COL_HEART_RATE = 'heart_rate'
COL_HR_ROLLING_3H_AVG = 'heart_rate_rolling_avg_3H'
COL_HR_ROLLING_1H_AVG = 'heart_rate_rolling_avg_1H'
COL_DATE = 'date'
COL_DATETIME = 'DateTime'

chronometer_macro_cols = ['Energy (kcal)', 'Protein (g)', 'Net Carbs (g)', 'Fat (g)']


def get_time_of_day(hour):
    if 6 <= hour < 12:  # 6 AM to 12 PM
        return 'morning'
    elif 12 <= hour < 18:  # 12 PM to 6 PM
        return 'afternoon'
    else:  # 6 PM to 6 AM
        return 'evening'


def get_daily_summaries(chronometer_macro_cols, df_recent):
    # Daily summaries for nutrition and heart rate
    daily_summary = df_recent.groupby(COL_DATE).agg(
        avg_heart_rate=(COL_HEART_RATE, 'mean'),
        max_heart_rate=(COL_HEART_RATE, 'max'),
        avg_heart_rate_1H=(COL_HR_ROLLING_1H_AVG, 'mean'),
        avg_heart_rate_3H=(COL_HR_ROLLING_3H_AVG, 'mean'),
        total_sugar_g=(COL_SUGAR, 'sum'),
        total_dairy_consumed_today=(COL_DAIRY, 'sum')  # Assuming 'dairy' is 1 for dairy, 0 for non-dairy
        # Add your Chronometer macros if present in df
    ).reset_index()
    # If Chronometer macros are available in df_recent, aggregate them too
    for col in chronometer_macro_cols:
        if col in df_recent.columns:
            daily_summary[col.lower().replace(' (kcal)', '_kcal').replace(' (g)', '_g').replace(' ', '_')] = \
                df_recent.groupby(COL_DATE)[col].sum().values  # Get sum for the day
            print(daily_summary)
    return daily_summary


def format_macro_nutrient(col):
    return col.lower().replace(' (kcal)', '_kcal').replace(' (g)', '_g').replace(' ', '_')

def load_user_profile(file_path) -> dict:
    if not os.path.exists(file_path):
        print(f"PATH: {file_path}")
        raise FileNotFoundError(f"User profile file not found: {file_path}")
    try:
        with open(file_path, 'r') as f:
            user_profile = json.load(f)
        return user_profile
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from profile file {file_path}: {e.msg}", e.doc, e.pos)
    except Exception as e:
        raise Exception(f"An unexpected error occurred while loading profile from {file_path}: {e}")


def analyze_food_heart_rate_impact(df_data, hr_threshold, window_minutes):
    """
    Analyzes which food items are frequently consumed before high heart rate episodes.
    """
    food_hr_correlations = {}

    # Iterate through each food entry
    for idx, food_row in df_data[df_data[COL_FOOD_NAME].notna()].iterrows():
        food_time = idx
        window_start = food_time
        window_end = food_time + pd.Timedelta(minutes=window_minutes)

        # Get heart rate data within this window
        hr_in_window = df_data.loc[window_start:window_end, COL_HEART_RATE].dropna()

        if not hr_in_window.empty:
            # Check if any heart rate value in the window exceeds the threshold
            if (hr_in_window > hr_threshold).any():
                food_name = food_row[COL_FOOD_NAME]
                if food_name not in food_hr_correlations:
                    food_hr_correlations[food_name] = 0
                food_hr_correlations[food_name] += 1

    # Sort by frequency
    sorted_correlations = sorted(food_hr_correlations.items(), key=lambda item: item[1], reverse=True)

    return sorted_correlations
