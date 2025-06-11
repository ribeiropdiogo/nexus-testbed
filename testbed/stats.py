"""
This modules contains the code responsible for generating statistics
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
        "average similarity": avg_cat_similarity
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
        "average similarity": avg_con_similarity,
        "average euclidean similarity": avg_euc_similarity,
        "average manhattan similarity": avg_man_similarity,
        "average canberra similarity": avg_can_similarity
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
        "average string similarity": avg_str_similarity,
        "average jaro-winkler similarity": avg_jw_similarity,
        "average sorensen-dice similarity": avg_sd_similarity,
        "average damerau-levenshtein similarity": avg_dl_similarity
    }
    # Return the output
    return output

def calculate_heterogeneous_stats(results_path: str, filename: str, rounds: int):
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
        # Iterate results
        for result in data['results']:
            # Check the datatype and sum the metrics accordingly
            if result['datatype'] == "categorical":
                direct_comp += result['metrics']['direct-comparison']
            elif result['datatype'] == "continuous":
                euclidean += result['metrics']['euclidean-distance']
                manhattan += result['metrics']['manhattan-distance']
                canberra += result['metrics']['canberra-distance']
            elif result['datatype'] == "string":
                jw += result['metrics']['jaro-winkler']
                sd += result['metrics']['sorensen-dice']
                dl += result['metrics']['damerau-levenshtein']
    # Calculate the average similarity for categorical data
    avg_cat_similarity = direct_comp / int(rounds)
    # Calculate the average similarity for continuous data
    avg_euc_similarity = 1 - (euclidean / int(rounds))
    avg_man_similarity = 1 - (manhattan / int(rounds))
    avg_can_similarity = 1 - (canberra / int(rounds))
    avg_con_similarity = (avg_euc_similarity + avg_man_similarity + avg_can_similarity) / 3
    # Calculate the average similarity for string data
    avg_jw_similarity = jw / int(rounds)
    avg_sd_similarity = sd / int(rounds)
    avg_dl_similarity = dl / int(rounds)
    avg_str_similarity = (avg_jw_similarity + avg_sd_similarity + avg_dl_similarity) / 3
    # Calculate overall average similarity
    avg_similarity = (avg_cat_similarity + avg_con_similarity + avg_str_similarity) / 3
    # Generate the output
    output = {
        "test": f"{filename}",
        "rounds": int(rounds),
        "datatype": "heterogeneous",
        "average similiarty": avg_similarity,
        "categorical": {
            "average similarity": avg_cat_similarity,
        },
        "continuous": {
            "average similarity": avg_con_similarity,
            "average euclidean similarity": avg_euc_similarity,
            "average manhattan similarity": avg_man_similarity,
            "average canberra similarity": avg_can_similarity
        },
        "string": {
            "average similarity": avg_str_similarity,
            "average jaro-winkler similarity": avg_jw_similarity,
            "average sorensen-dice similarity": avg_sd_similarity,
            "average damerau-levenshtein similarity": avg_dl_similarity
        }
    }
    # Return the output
    return output

if __name__ == "__main__":
    # # Extract command line arguments
    algorithm = sys.argv[1]
    datatype  = sys.argv[2]
    filename  = sys.argv[3]
    rounds    = sys.argv[4]
    # Build the results path
    results_path = f"./results/{datatype}/{algorithm}/"
    # Check the datatype and calculate statistics accordingly
    if datatype == "categorical":
        output = calculate_categorical_stats(results_path, filename, rounds)
    elif datatype == "continuous":
        output = calculate_continuous_stats(results_path, filename, rounds)
    elif datatype == "string":
        output = calculate_string_stats(results_path, filename, rounds)
    elif datatype == "heterogeneous":
        output = calculate_heterogeneous_stats(results_path, filename, rounds)
    else:
        # Raise an error for unknown datatype
        raise ValueError(f"Unknown datatype: {datatype}")

    # Build the stats output path
    output_path = f"./stats/{datatype}/{algorithm}/"
    # Create the output directory if it does not exist
    os.makedirs(output_path, exist_ok=True)
    # Build the stats output filepath
    output_file = f"{output_path}{filename}.json"
    # Dump the output to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
