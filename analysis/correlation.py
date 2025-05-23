import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def correlation_matrix(df_merged, output_folder):

    correlation_data = df_merged[['heart_rate', 'dairy_consumed_last_3_days', 'total_sugar_consumed_today', 'days_since_last_dairy']]  # Add other food features as needed

    # Calculate the correlation matrix
    corr_matrix = correlation_data.corr()

    # Visualize the correlation matrix using a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')  # annot=True displays the correlation coefficients
    plt.title('Correlation Matrix of Food Features and Heart Rate')
    plt.savefig(output_folder+'plot_correlation')

    # Print the correlation matrix for text output
    print("Correlation Matrix:\n", corr_matrix)



def scatterplot(df_merged, output_folder):
    # Scatter plot: Sugar vs. Heart Rate
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='dairy_consumed_last_3_days', y='heart_rate', data=df_merged)
    plt.title('Dairy Consumption vs. Heart Rate')
    plt.xlabel('Dairy Consumed Today (0: No, 1: Yes)')
    plt.ylabel('Heart Rate (bpm)')
    plt.savefig(output_folder+'plot_scatter.png')

    # Scatter plot: Sugar vs. Heart Rate
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='total_sugar_consumed_today', y='heart_rate', data=df_merged)
    plt.title('Sugar Consumption vs. Heart Rate')
    plt.xlabel('Total Sugar Consumed Today (g)')
    plt.ylabel('Heart Rate (bpm)')
    plt.savefig(output_folder+'plot_scatter_sugar.png')