# Health Data Analyzer

A Python-based tool for analyzing personal health data from Garmin devices and Cronometer food logs, providing insights through data analysis and AI-powered recommendations.

## Features

- Processes and analyzes Garmin FIT files for health metrics
- Cleans and processes Cronometer food servings data
- Performs feature engineering on combined health and nutrition data
- Generates visualizations including:
  - Data plots
  - Correlation matrices
  - Scatterplots
- Trains a linear regression model for health metrics analysis
- Provides AI-powered health insights using Ollama LLM

## Prerequisites

- Python 3.x
- Ollama installed and running locally
- Garmin FIT files
- Cronometer food servings export (CSV format)

## Installation

1. Clone this repository
2. Install required dependencies (requirements.txt recommended)
3. Ensure Ollama is installed and the specified model is available

## Usage

Run the analyzer using the following commands: 
`python -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`
`python main.py`




### Command Line Options

- `--fit_dir`: Directory containing Garmin FIT files (default: 'data/raw/garmin')
- `--input_food_file`: Path to raw Cronometer food servings CSV (default: 'data/raw/servings.csv')
- `--output_food_file`: Path for cleaned food data (default: 'data/clean/servings.csv.bak')
- `--output_folder`: Directory for analysis outputs (default: 'data/output/')
- `--ollama_model`: Ollama model name (default: 'granite3.3:2b')
- `--analysis_days`: Number of days to analyze (default: 11)
- `--profile_path`: Path to user profile JSON (default: 'data/profiles/user_profile.json')

## Data Structure

### Required Input Files

1. Garmin FIT files in the specified directory
2. Cronometer food servings CSV file
3. User profile JSON file containing personal health parameters

### Output

The tool generates:
- Cleaned data files
- Visualization plots
- Correlation analysis
- Machine learning model results
- AI-generated health insights

## Features Analysis

The tool analyzes various health metrics including:
- Heart rate data (including rolling averages)
- Dairy consumption patterns
- Sugar intake
- Time-of-day effects
- Macro-nutrient tracking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

GNU General Public License v3.0