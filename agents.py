## agents.py : takes sample dataset file in a csv format 
## agent will create a new synthetic data file in csv .

# Importing Libraries

import os
import csv
import anthropic ## Anthropic SDK Package for API endpoints.
from prompts import *

# Setting up Anthropic API Key.

if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Enter your API Key: ")

# Creating client
client = anthropic.Anthropic()
sonnet = "claude-3-5-sonnet-20240620" # Name of the model fullname of its API.

# Reading CSV file from the client:
def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline="") as csvfile: # open csv file in read mode.
        csv_reader = csv.reader(csvfile) # creating a csv reading object.
        for row in csv_reader:
            data.append(row) # adding each row to the python data list
    print(data)
    return data

# Function for Saving the newly generated csv file with new data.
def save_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a' # 
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in csv.reader(data.splitlines()): # splitlines() method in Python is a built-in string method that splits a string at line breaks and returns a list of lines in the string.
            writer.writerow(row)

def analyzer_agent(sample_data):
    message = client.messages.create(
        model=sonnet,
        max_tokens=400, # Limit the response to 400 tokens
        temperature=0.1, # Randomness, set a low temperature for more focused, deterministic output
        system=ANALYZER_SYSTEM_PROMPT, #use the predefined system prompt for the analyzer
        messages=[
            {
                "role": "user",
                "content":ANALYZER_USER_PROMPT.format(sample_data=sample_data) # # Format the user prompt with the provided sample data
            }
        ]
    )
    print(message.content)
    return message.content[0].text # Return the text content of the first message only.


def generator_agent(analysis_result, sample_data, num_rows=30):
    #print(analysis_result)
    message = client.messages.create(
        model=sonnet,
        max_tokens=1500,# Response should be higher
        temperature=1, # To generate new data , randomness should be high.
        system=GENERATOR_SYSTEM_PROMPT,
        messages = [
            {
                "role":"user",
                "content":GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data
                )
            }
        ]
    )


file_name = input("\nEnter the name of your CSV File: ")
file_path = os.path.join('/app/data', file_name)
input_rows = int(input("Enter the number of rows in dataset you want to generate: "))

# Reading Sample CSV
sample_data = read_csv(file_path) # outputs list of lists
sample_data_str = "\n".join([",".join(row) for row in sample_data]) # Convert 2D List to a single string.

print("\nSynthetic Data Agent is Readying...")
# First we Analyze the Data:
analysis_result = analyzer_agent(sample_data_str)
print("\n### Analyzer Agent Output: ###\n")
print(analysis_result)
print("\n------------------------------------------------\n\nGenerating new Data...")

#Set up the output File:---
output_file = "/app/data/new_dataset.csv"
headers = sample_data[0] # Getting headers from the sample data, headers are Index 0 .
#create the output file with headers
save_csv("",output_file, headers) # creating/Initializing empty output file with the header only with no dataset , dataset will be added by generator agent.

batch_size = 30 #Sets a batch size for generating data in chunks to manage memory usage efficiently., Number of rows to generate in a single Batch.
generated_rows = 0

while generated_rows < input_rows:
    rows_to_generate = min(batch_size, input_rows - generated_rows)

    GeneratedData = generator_agent(analysis_result, sample_data_str, rows_to_generate)

    save_csv(GeneratedData, output_file)

    generated_rows += rows_to_generate

    print(f"Generated {generated_rows} rows out of {input_rows}")

print(f"\n Your New Data Has been Generated and saved in output file {output_file}")