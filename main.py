import utils
from cleaners.cronometer_cleaner import clean_csv
from cleaners.garmin_fit_processor import process_fit_files
from analysis.ploting import plot
from analysis.data_llm_analyzer import ollama_processing
from cleaners.feature_engineering import augmented_data_features, merge_data
from analysis.correlation import correlation_matrix, scatterplot
from analysis.training import train_model
import argparse
import pandas as pd


def main(fit_directory: str,
    input_food_file: str,
    output_food_file: str,
    output_folder: str,
    ollama_model_name: str,
    analysis_duration_days: int,
    profile_file_path: str):
    """
        Main function to execute the health data analysis pipeline.

        Args:
            fit_directory (str): Path to the directory containing raw .fit files.
            input_food_file (str): Path to the raw Chronometer food servings CSV.
            output_food_file (str): Path to save the cleaned Chronometer servings CSV.
            output_folder (str): Directory where analysis outputs (e.g., LLM responses) will be saved.
            ollama_model_name (str): Name of the Ollama model to use for analysis.
            analysis_duration_days (int): Number of days to include in the data analysis.
             profile_file_path (str): Path to the file where the LLM profile will be saved.
        """

    print("Starting metrics analyzer with:")
    print(f"  FIT Directory: {fit_directory}")
    print(f"  Input Food File: {input_food_file}")
    print(f"  Output Food File: {output_food_file}")
    print(f"  Output Folder: {output_folder}")
    print(f"  Ollama Model: {ollama_model_name}")

    # Execute cleaning logic
    clean_csv(input_food_file, output_food_file)
    df_garmin = process_fit_files(fit_directory)
    df_garmin = df_garmin.sort_values(by='timestamp')

    if df_garmin is not None:
        print(df_garmin.head().to_markdown(index=False, numalign="left", stralign="left"))
        print(df_garmin.info())

    # Load the cleaned Cronometer data
    df_food = pd.read_csv(output_food_file)
    df_food[utils.COL_DATETIME] = pd.to_datetime(df_food[utils.COL_DATETIME], utc=True)  # Convert to UTC
    df_food = df_food.sort_values(by=utils.COL_DATETIME)

    df_merged = merge_data(df_food, df_garmin)
    df_merged = augmented_data_features(df_merged)


    plot(df_merged, output_folder)

    correlation_matrix(df_merged, output_folder)
    scatterplot(df_merged, output_folder)
    linear_result = train_model(df_merged)

    profile = utils.load_user_profile(profile_file_path)
    ollama_processing(profile, ollama_model_name, df_merged, linear_result, analysis_duration_days)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze Garmin and Chronometer health data with a local LLM."
    )

    parser.add_argument(
        '--fit_dir',
        type=str,
        default='data/raw/garmin',
        help='Path to the directory containing raw .fit files.'
    )
    parser.add_argument(
        '--input_food_file',
        type=str,
        default="data/raw/servings.csv",
        help='Path to the raw Chronometer food servings CSV.'
    )
    parser.add_argument(
        '--output_food_file',
        type=str,
        default="data/clean/servings.csv.bak",
        help='Path to save the cleaned Chronometer servings CSV.'
    )
    parser.add_argument(
        '--output_folder',
        type=str,
        default="data/output/",
        help='Directory where analysis outputs (e.g., LLM responses) will be saved.'
    )
    parser.add_argument(
        '--ollama_model',
        type=str,
        default='granite3.3:2b',
        help='Name of the Ollama model to use for analysis (e.g., "granite3.3:2b").'
    )
    parser.add_argument(
        '--analysis_days',
        type=int,
        default=11,
        help='Number of days to include in the data analysis for LLM summary.'
    )
    parser.add_argument(
        '--profile_path',
        type=str,
        default='data/profiles/user_profile.json',
        help='Path to the file where the LLM profile will be saved.'
    )

    args = parser.parse_args()

    main(
        fit_directory=args.fit_dir,
        input_food_file=args.input_food_file,
        output_food_file=args.output_food_file,
        output_folder=args.output_folder,
        ollama_model_name=args.ollama_model,
        analysis_duration_days=args.analysis_days,
        profile_file_path=args.profile_path
    )
