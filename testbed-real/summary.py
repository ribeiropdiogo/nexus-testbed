"""
This module contains the code responsible for generating a summary of
the statistics in csv format.
"""

import sys
import os
import json

def custom_sort_key(test_name):
    """
    Custom sort key for test names.
    """
    # Assumes format like 's5_n1'
    parts = test_name.split('_')
    s_part = int(parts[0][1:])  # after 's'
    n_part = int(parts[1][1:])  # after 'n'
    return (s_part, n_part)

if __name__ == "__main__":
    # Extract command line arguments
    datatype = sys.argv[1]
    # Build the stats path
    stats_path = f"./stats/{datatype}/"
    # Initialize algorithms and files list
    algorithms = []
    tests      = set()
    # Iterate through the algorithms in the stats path
    for folder_name in os.listdir(stats_path):
        # Build the folder path
        folder_path = os.path.join(stats_path, folder_name)
        # Check if the path is a directory
        if os.path.isdir(folder_path):
            # Save the algorithms
            algorithms.append(folder_name)
            # Iterate through the files in the folder
            for file_name in os.listdir(folder_path):
                # Check if the file is a json file
                if file_name.endswith('.json'):
                    # Add the file to the set
                    tests.add(file_name[:-5])
    
    # Sort the tests using the custom sort key
    tests = sorted(tests, key=custom_sort_key)
    # Create the stats directory if it doesn't exist
    os.makedirs("./stats/csv", exist_ok=True)
    # Build the stats output path
    with open(f"./stats/csv/{datatype}.csv", "w", encoding="utf-8") as csvfile:
        # Print the header
        csvfile.write("test,algorithm,direct comparison,euclidean,manhattan,canberra,jaro-winkler,sorensen-dice,damerau-levenshtein\n")
        # Iterate through the tests and algorithms
        for file in tests:
            for algorithm in algorithms:
                # Build the stats input path
                input_path = f"./stats/{datatype}/{algorithm}/{file}.json"
                # Read the json file
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                    # Parse the json data
                    stats = json.loads(data)
                    # Extract the statistics
                    dc = stats.get('categorical', {}).get("average similarity", "")
                    eu = stats.get('continuous', {}).get("average euclidean similarity", "")
                    mn = stats.get('continuous', {}).get("average manhattan similarity", "")
                    cb = stats.get('continuous', {}).get("average canberra similarity", "")
                    jw = stats.get('string', {}).get("average jaro-winkler similarity", "")
                    sd = stats.get('string', {}).get("average sorensen-dice similarity", "")
                    dl = stats.get('string', {}).get("average damerau-levenshtein similarity", "")

                # Read the stats file
                csvfile.write(f"{file},{algorithm},{dc},{eu},{mn},{cb},{jw},{sd},{dl}\n")
