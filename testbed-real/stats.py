"""
This module contains the code responsible for generating statistics
from the results of the various algorithms executions.
"""

import sys
import os
import json


def calculate_categorical_stats(results_path: str, filename: str, rounds: int):
    """
    Calculate the average similarity for categorical data.
    """
    # Initialize statistics variables
    avg_cat_similarity = 0
    # Initialize counters
    direct_comp = 0
    # Iterate over the rounds
    for i in range(int(rounds)):
        # Build the filename
        datafile = f"{results_path}{filename}_{i+1}.json"
        # Check if the file exists
        if not os.path.exists(datafile):
            print(f"File {datafile} does not exist.")
            # Print error message and exit the program
            sys.exit(f"File {datafile} does not exist.")
        # Read the file
        with open(datafile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Sum the direct comparison metric
        direct_comp += data['results'][0]['metrics']['direct-comparison']

    # Calculate the average similarity
    avg_cat_similarity = direct_comp / int(rounds)
    # Generate the output
    output = {
        "test": f"{filename}",
        "rounds": int(rounds),
        "datatype": "categorical",
        "categorical": {
            "average similarity": avg_cat_similarity
        }
    }
    # Return the output
    return output

def calculate_continuous_stats(results_path: str, filename: str, rounds: int):
    """
    Calculate the average similarity for continuous data.
    """
    # Initialize statistics variables
    avg_con_similarity = 0
    avg_euc_similarity = 0
    avg_man_similarity = 0
    avg_can_similarity = 0
    # Initialize counters
    euclidean = 0
    manhattan = 0
    canberra  = 0
    # Iterate over the rounds
    for i in range(int(rounds)):
        # Build the filename
        datafile = f"{results_path}{filename}_{i+1}.json"
        # Check if the file exists
        if not os.path.exists(datafile):
            print(f"File {datafile} does not exist.")
            # Print error message and exit the program
            sys.exit(f"File {datafile} does not exist.")
        # Read the file
        with open(datafile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Sum the metrics
        euclidean += data['results'][0]['metrics']['euclidean-distance']
        manhattan += data['results'][0]['metrics']['manhattan-distance']
        canberra  += data['results'][0]['metrics']['canberra-distance']
    # Calculate the average similarity
    avg_euc_similarity = 1 - (euclidean / int(rounds))
    avg_man_similarity = 1 - (manhattan / int(rounds))
    avg_can_similarity = 1 - (canberra / int(rounds))
    avg_con_similarity = (avg_euc_similarity + avg_man_similarity + avg_can_similarity) / 3
    # Generate the output
    output = {
        "test": f"{filename}",
        "rounds": int(rounds),
        "datatype": "continuous",
        "continuous": {
            "average similarity": avg_con_similarity,
            "average euclidean similarity": avg_euc_similarity,
            "average manhattan similarity": avg_man_similarity,
            "average canberra similarity": avg_can_similarity
        }
    }
    # Return the output
    return output

def calculate_string_stats(results_path: str, filename: str, rounds: int):
    """
    Calculate the average similarity for string data.
    """
    # Initialize statistics variables
    avg_str_similarity = 0
    avg_jw_similarity = 0
    avg_sd_similarity = 0
    avg_dl_similarity = 0
    # Initialize counters
    jw = 0
    sd = 0
    dl = 0
    # Iterate over the rounds
    for i in range(int(rounds)):
        # Build the filename
        datafile = f"{results_path}{filename}_{i+1}.json"
        # Check if the file exists
        if not os.path.exists(datafile):
            print(f"File {datafile} does not exist.")
            # Print error message and exit the program
            sys.exit(f"File {datafile} does not exist.")

        # Read the file
        with open(datafile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Sum the metrics
        jw += data['results'][0]['metrics']['jaro-winkler']
        sd += data['results'][0]['metrics']['sorensen-dice']
        dl += data['results'][0]['metrics']['damerau-levenshtein']
    
    # Calculate the average similarity
    avg_jw_similarity = jw / int(rounds)
    avg_sd_similarity = sd / int(rounds)
    avg_dl_similarity = dl / int(rounds)
    avg_str_similarity = (avg_jw_similarity + avg_sd_similarity + avg_dl_similarity) / 3
    # Generate the output
    output = {
        "test": f"{filename}",
        "rounds": int(rounds),
        "datatype": "string",
        "string": {
            "average similarity": avg_str_similarity,
            "average jaro-winkler similarity": avg_jw_similarity,
            "average sorensen-dice similarity": avg_sd_similarity,
            "average damerau-levenshtein similarity": avg_dl_similarity
        }
    }
    # Return the output
    return output

def calculate_heterogeneous_stats(results_path: str, dir: str):
    """
    Calculate the average similarity for heterogeneous data.
    """
    # Initialize statistics variables
    avg_cat_similarity = 0
    avg_con_similarity = 0
    avg_euc_similarity = 0
    avg_man_similarity = 0
    avg_can_similarity = 0
    avg_str_similarity = 0
    avg_jw_similarity  = 0
    avg_sd_similarity  = 0
    avg_dl_similarity  = 0
    # Initialize counters
    direct_comp = 0
    euclidean = 0
    manhattan = 0
    canberra = 0
    jw = 0
    sd = 0
    dl = 0
    # Datatype counter
    cat_count = 0
    con_count = 0
    str_count = 0
    # Flags to check if data types are present
    has_categorical = False
    has_continuous  = False
    has_string      = False
    # Initialize rounds counter
    rounds = 0
    # Iterate over the round dirs
    for round in os.listdir(dir):
        # Build the metrics directory path
        metrics_dir = f"{dir}/{round}/metrics/"
        # Iterate files in dir to get filename
        for file in os.listdir(metrics_dir):
            if file.endswith(".json"):
                path = os.path.join(metrics_dir, file)
                # Check if the file exists
                if not os.path.exists(path):
                    print(f"File {file} does not exist.")
                    # Print error message and exit the program
                    sys.exit(f"File {file} does not exist.")
                # Read the file
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Iterate results
                for result in data['results']:
                    # Check the datatype and sum the metrics accordingly
                    if result['datatype'] == "categorical":
                        has_categorical = True
                        cat_count += 1
                        direct_comp += result['metrics']['direct-comparison']
                    elif result['datatype'] == "continuous":
                        has_continuous = True
                        con_count += 1
                        euclidean += result['metrics']['euclidean-distance']
                        manhattan += result['metrics']['manhattan-distance']
                        canberra += result['metrics']['canberra-distance']
                    elif result['datatype'] == "string":
                        has_string = True
                        str_count += 1
                        jw += result['metrics']['jaro-winkler']
                        sd += result['metrics']['sorensen-dice']
                        dl += result['metrics']['damerau-levenshtein']
        rounds += 1
    # Calculate the average similarity for categorical data
    if has_categorical:
        avg_cat_similarity = (direct_comp/cat_count)
    # Calculate the average similarity for continuous data
    if has_continuous:
        avg_euc_similarity = 1 - ((euclidean/con_count))
        avg_man_similarity = 1 - ((manhattan/con_count))
        avg_can_similarity = 1 - ((canberra/con_count))
        avg_con_similarity = (avg_euc_similarity + avg_man_similarity + avg_can_similarity) / 3
    # Calculate the average similarity for string data
    if has_string:
        avg_jw_similarity = (jw/str_count)
        avg_sd_similarity = (sd/str_count)
        avg_dl_similarity = (dl/str_count)
        avg_str_similarity = (avg_jw_similarity + avg_sd_similarity + avg_dl_similarity) / 3
    # Calculate overall average similarity
    types = sum([has_categorical, has_continuous, has_string])
    avg_similarity = (avg_cat_similarity + avg_con_similarity + avg_str_similarity) / types
    # Generate the output
    output = {
        "test": f"{results_path}",
        "rounds": int(rounds),
        "datatype": "heterogeneous",
        "average similarity": avg_similarity,
        "categorical": {
            "average similarity": avg_cat_similarity,
        } if has_categorical else {},
        "continuous": {
            "average similarity": avg_con_similarity,
            "average euclidean similarity": avg_euc_similarity,
            "average manhattan similarity": avg_man_similarity,
            "average canberra similarity": avg_can_similarity
        } if has_continuous else {},
        "string": {
            "average similarity": avg_str_similarity,
            "average jaro-winkler similarity": avg_jw_similarity,
            "average sorensen-dice similarity": avg_sd_similarity,
            "average damerau-levenshtein similarity": avg_dl_similarity
        } if has_string else {}
    }
    
    # Return the output
    return output

if __name__ == "__main__":
    # # Extract command line arguments
    dataset  = sys.argv[1]
    input    = sys.argv[2]
    print(f" > Dataset: {dataset}")
    print(f" > Input: {input}")

    # Build the results path
    results_path = f"./results-real/{dataset}/"
    # Calculate the stats
    output = calculate_heterogeneous_stats(results_path, input)
    # Build the stats output path
    output_path = input.replace("results", "stats")
    # Create the output directory if it does not exist
    os.makedirs(output_path, exist_ok=True)
    # Build the stats output filepath
    output_file = f"{output_path}results.json"
    # Dump the output to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
