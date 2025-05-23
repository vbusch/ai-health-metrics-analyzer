import seaborn as sns
from matplotlib import pyplot as plt

from utils import COL_FOOD_NAME, COL_SUGAR_TODAY, COL_SUGAR, COL_SINCE_LAST_DAIRY, COL_DAIRY_LAST_CONSUMED_DAYS, \
    COL_DAIRY, COL_HR_ROLLING_3H_AVG, COL_HR_ROLLING_1H_AVG, COL_HEART_RATE, COL_DATETIME, COL_DATE


def plot(df_merged, output_folder):
    # Display the result
    print(df_merged[[COL_DATETIME, COL_HEART_RATE, COL_HR_ROLLING_1H_AVG, COL_HR_ROLLING_3H_AVG,  COL_FOOD_NAME, COL_DAIRY, COL_DATE, COL_DAIRY_LAST_CONSUMED_DAYS,
                     COL_SINCE_LAST_DAIRY, COL_SUGAR, COL_SUGAR_TODAY, 'time_morning', 'time_afternoon', 'time_evening', 'Energy (kcal)']].head(20).to_markdown(
        index=False, numalign="left", stralign="left"))
    # Plot heart rate over time
    plt.figure(figsize=(12, 6))  # Adjust figure size as needed
    sns.lineplot(x=COL_DATETIME, y=COL_HEART_RATE, data=df_merged)
    plt.title('Heart Rate Over Time')
    plt.xlabel('Date and Time')
    plt.ylabel('Heart Rate (bpm)')
    plt.savefig(output_folder+'plot_heart_rate.png')

    # plot rolling average (e.g., 1-hour rolling average)
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=COL_DATETIME, y=COL_HR_ROLLING_1H_AVG, data=df_merged)
    plt.title('1-Hour Rolling Average Heart Rate')
    plt.xlabel('Date and Time')
    plt.ylabel('Heart Rate (bpm)')
    plt.savefig(output_folder+'plot_heart_rate_rolling_avg.png')
