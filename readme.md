# Synthetic Data Generator Documentation

## Overview

This project consists of a synthetic data generation agent that uses the Anthropic API to analyze and generate new data based on a given sample CSV file. The generated data is saved in a new CSV file.

## Project Structure

- **agents.py**: The main script for reading the sample CSV file, analyzing it using the Anthropic API, and generating new synthetic data.
- **prompts.py**: Contains the prompt templates used for data analysis and generation.
- **Dockerfile**: Docker configuration file for setting up the container environment.
- **requirements.txt**: Lists the Python dependencies required for the project.

## Setup

### Prerequisites

- Docker
- Anthropic API Key

### Directory Structure

Ensure your project directory has the following structure:
```
/project-root
│── agents.py
│── prompts.py
│── Dockerfile
│── requirements.txt
│── data/
    └── fineTuningSampleDataset.csv
```

### Configuration

1. **Anthropic API Key**: Ensure you have your Anthropic API Key ready as it will be needed during execution.

2. **Sample CSV File**: Place your sample CSV file (e.g., `fineTuningSampleDataset.csv`) in the `data` directory.

### Build Docker Image

Navigate to the project directory and build the Docker image using the following command:
```
docker build -t synthetic-data-agent .
```

## Usage

### Running the Docker Container

Run the Docker container with the necessary volume mounting and execute the script:
```sh
docker run -it -v "/path/to/project-root/data:/app/data" synthetic-data-agent
```

Replace `/path/to/project-root` with the actual path to your project directory on the host machine.

### Execution Steps

1. **API Key**: When prompted, enter your Anthropic API Key.
2. **CSV File**: Enter the name of your CSV file (e.g., `fineTuningSampleDataset.csv`).
3. **Number of Rows**: Enter the number of rows you want to generate (e.g., 65).

### Expected Output

The script will read the sample CSV file, analyze it, and generate the specified number of new rows. The generated data will be saved in a new CSV file (`new_dataset.csv`) in the `data` directory.

## Code Explanation

### agents.py

This script contains the following functions:

- **read_csv(file_path)**: Reads the sample CSV file and returns its contents as a list of lists.
- **save_csv(data, output_file, headers=None)**: Saves the provided data into a CSV file. If headers are provided, they are written to the file first.
- **analyzer_agent(sample_data)**: Sends the sample data to the Anthropic API for analysis and returns the analysis results.
- **generator_agent(analysis_result, sample_data, num_rows=30)**: Sends the analysis results and sample data to the Anthropic API to generate new data and returns the generated rows.

### prompts.py

This script contains the prompt templates used for data analysis and generation:

- **ANALYZER_SYSTEM_PROMPT**: Prompt for the analyzer agent.
- **GENERATOR_SYSTEM_PROMPT**: Prompt for the generator agent.
- **ANALYZER_USER_PROMPT**: User prompt for the analyzer agent.
- **GENERATOR_USER_PROMPT**: User prompt for the generator agent.

### Dockerfile

The Dockerfile sets up the Python environment with the necessary dependencies and copies the project files into the container.

### requirements.txt

Lists the Python dependencies required for the project, including the `anthropic` package for interacting with the Anthropic API.