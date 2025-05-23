import json
import os

import ollama
import pandas as pd

from utils import COL_FOOD_NAME, get_daily_summaries, COL_DAIRY, COL_DATETIME, format_macro_nutrient, \
    chronometer_macro_cols, \
    analyze_food_heart_rate_impact, COL_DATE


def ollama_processing(user_profile, ollama_model_name, df, linear_result, analysis_days=32):

    today = pd.Timestamp.utcnow()
    start_date = today - pd.Timedelta(days=analysis_days)
    end_date = today
    df = df.set_index(COL_DATETIME)
    df_recent = df[(df.index >= start_date) & (df.index <= end_date)]
    if df_recent.empty:
        print(
            f"No data available for the last {analysis_days} days. Please adjust the analysis range or provide more recent data.")
        exit()

    data_json_string = df_recent.to_json(orient='records', indent=2)
    full_profile_context = create_profile_str(user_profile)
    daily_summary = get_daily_summaries(chronometer_macro_cols, df_recent)
    dairy_consumption_info = create_dairy_consumption_info(df_recent)
    food_summary = create_top_food_summary(df_recent)
    hr_impact_summary = create_heart_rate_impact_summary(df_recent, user_profile)
    daily_summary_markdown = daily_summary.to_markdown(index=False)


    # Generate LLM-ready text summary
    llm_data_summary = f"""
    Here is a summary of my health and nutritional data for the last {analysis_days} days ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):
    
    Daily Averages:
    - Average Heart Rate: {daily_summary['avg_heart_rate'].mean():.1f} bpm
    - Average 1-Hour Rolling Heart Rate: {daily_summary['avg_heart_rate_1H'].mean():.1f} bpm
    - Average 3-Hour Rolling Heart Rate: {daily_summary['avg_heart_rate_3H'].mean():.1f} bpm
    - Total Sugars Consumed Daily: {daily_summary['total_sugar_g'].mean():.1f}g
    
    {create_daily_avg_macro_nutrient(daily_summary)}
    
    {full_profile_context}
    
    Here's a detailed daily summary of my health data for the last {analysis_days} days:
    {daily_summary_markdown}
    
    {food_summary}
    {dairy_consumption_info}
    
    {hr_impact_summary} 
    
    Do you know the linear regression coefficients in regards to:
         - dairy_consumed_last_3_days
        - total_sugar_consumed_today
        - time_morning
        - time_afternoon
        - time_evening
    """
    # {json_string}

    # Also a Linear Regression Result: {linear_result}
    # 
    # Based on this data, please provide actionable recommendations...
    # Also, can you explain the linear regression result?
    # 
    # """

    print("\n--- LLM-Ready Data Summary ---")
    print(llm_data_summary)

    prompt = f"""
        {llm_data_summary}

    """

    try:
        response = ollama.chat(
            model=ollama_model_name,
            messages=[
                {'role': 'system',
                 'content': 'You are a helpful AI nutritionist and fitness coach. Analyze user data and goals to provide evidence-based, actionable dietary, cardiovascular, and general health recommendations. Focus on practical advice and avoid medical diagnoses.'},
                {'role': 'user', 'content': prompt}
            ],
            stream=False
        )
        print("\n--- LLM Recommendations ---")
        print(response['message']['content'])

    except ollama.ResponseError as e:
        print(f"Ollama Error: {e}")
        print(
            f"Ensure Ollama server is running (e.g., `ollama serve` in a terminal) and the '{ollama_model_name}'granite3.3:2b'' model is pulled.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def create_daily_avg_macro_nutrient(daily_summary):
    result = ""
    for col in chronometer_macro_cols:

        formatted_col = format_macro_nutrient(col)
        if formatted_col in daily_summary.columns:  # Check if the aggregated column exists
            result += f"- Average Daily {col.replace(' (kcal)', '').replace(' (g)', '')}: {daily_summary[format_macro_nutrient(col)].mean():.1f}{'kcal' if 'kcal' in col else 'g'}\n"
    return result


def create_top_food_summary(df_recent):
    top_foods = df_recent[COL_FOOD_NAME].value_counts().head(5).index.tolist()
    food_summary = f"Top 5 most consumed food items: {', '.join(top_foods)}."
    return food_summary


def create_dairy_consumption_info(df_recent):
    # Identify days with dairy consumption
    dairy_days = df_recent[df_recent[COL_DAIRY] > 0][COL_DATE].unique()
    dairy_consumption_info = f"Dairy was consumed on {len(dairy_days)} out of {df_recent[COL_DATE].nunique()} days in the analysis period."
    dairy_consumption_info += f" Last consumption on {pd.Series(dairy_days).max().strftime('%Y-%m-%d')}."
    return dairy_consumption_info


def create_profile_str(user_profile):
    profile_str = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in user_profile.items()])
    full_profile_context = f"Here is my personal profile and goals:\n{profile_str}"
    return full_profile_context


def create_heart_rate_impact_summary(df_recent, user_profile):
    print(
        f"\nAnalyzing food impact on heart rate (threshold: {user_profile['high_heart_rate_threshold']}bpm, window: {user_profile['heart_rate_analysis_window_minutes']}min)...")
    potential_hr_impacting_foods = analyze_food_heart_rate_impact(
        df_recent,
        user_profile['high_heart_rate_threshold'],
        user_profile['heart_rate_analysis_window_minutes']
    )
    hr_impact_summary = ""
    if potential_hr_impacting_foods:
        hr_impact_summary = "Foods frequently consumed before high heart rate episodes (over {}bpm within {} minutes):\n".format(
            user_profile['high_heart_rate_threshold'], user_profile['heart_rate_analysis_window_minutes']
        )
        for food, count in potential_hr_impacting_foods[:5]:  # List top 5
            hr_impact_summary += f"- {food}: {count} occurrences\n"
        hr_impact_summary += "This suggests a *potential correlation* worth investigating, but not necessarily causation."
    else:
        hr_impact_summary = "No consistent food items found preceding high heart rate episodes within the defined window."
    return hr_impact_summary
