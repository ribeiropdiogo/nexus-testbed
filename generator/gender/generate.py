"""
Script to generate the diabetes dataset from the source data.
"""

import os
import json
import csv
import random

INPUT = "name_gender_dataset.csv"
DBENTRIES = 10
DBFIELDS  = 3
CLAIMS    = DBENTRIES * DBFIELDS


def add_str_noise(string):
    # Get string length
    length = len(string)
    # Get a random number of errors to introduce
    num_errors = random.randint(2, max(2, length // 5))
    # Get the positions of the errors
    error_positions = random.sample(range(length), num_errors)
    # Introduce the errors
    noisy_string = list(string)
    for pos in error_positions:
        char = random.choice("abcdefghijklmnopqrstuvwxyz")
        if char != noisy_string[pos]:
            noisy_string[pos] = char
    # Join the list back into a string
    noisy_string = "".join(noisy_string)
    # Remove a random word with a small probability
    if random.random() < 0.5:
        words = noisy_string.split()
        if len(words) > 1:
            remove_pos = random.randint(0, len(words) - 1)
            del words[remove_pos]
            noisy_string = " ".join(words)
    # Return the noisy string
    return noisy_string

def name_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = row['Name']
    # Initialize the object
    obj = {
        "name": "name_" + str(rowId),
        "datatype": "string",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            value = add_str_noise(truth)
            noisy_sources -= 1
        else:
            value = truth
        # Create entry object
        entry = {
            "sourceId": f"source{i+1}",
            "fact": value
        }
        # Append entry to claims
        obj["claims"].append(entry)
    # Append object to the dataset
    dataset["objects"].append(obj)

def gender_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = row['Gender']
    # Initialize the object
    obj = {
        "name": "gender_" + str(rowId),
        "datatype": "string",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            value = "M" if truth == "F" else "F"
            noisy_sources -= 1
        else:
            value = truth
        # Create entry object
        entry = {
            "sourceId": f"source{i+1}",
            "fact": value
        }
        # Append entry to claims
        obj["claims"].append(entry)
    # Append object to the dataset
    dataset["objects"].append(obj)

def count_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = int(row['Count'])
    # Initialize the object
    obj = {
        "name": "count_" + str(rowId),
        "datatype": "integer",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            noise = random.randint(-1 * truth, truth)
            while noise == 0:
                noise = random.randint(-1 * truth, truth)
            value = truth + noise
            noisy_sources -= 1
        else:
            value = truth
        # Create entry object
        entry = {
            "sourceId": f"source{i+1}",
            "fact": value
        }
        # Append entry to claims
        obj["claims"].append(entry)
    # Append object to the dataset
    dataset["objects"].append(obj)

def generate(noise: int, sources: int, output_path: str):
    """
    Open the source data and generate the dataset.
    """
    try:
        # Open the csv file
        with open("generator/gender/" + INPUT, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)
            print(f"\n > Number of individual claims: {CLAIMS * sources}")
            # Only iterate to max DBENTRIES
            data = data[:DBENTRIES]
            # Initialize counter
            rowId = 1
            # Iterate lines
            for row in data:
                # Initialize an empty structure for the row
                dataset = {
                    "objects": [],
                    "sources": []
                }
                # Add claims to structure
                name_entry(dataset, row, rowId, noise, sources)
                gender_entry(dataset, row, rowId, noise, sources)
                count_entry(dataset, row, rowId, noise, sources)
                # Build the output path
                output = os.path.join(output_path, f"s{sources}_n{noise}/subject{rowId}.json")
                # Ensure the output directory exists
                os.makedirs(os.path.dirname(output), exist_ok=True)
                # Save the dataset to the JSON file
                with open(output, "w", encoding='utf-8') as f:
                    json.dump(dataset, f, indent=4)
                # Increment rowId
                rowId += 1        
    except Exception as e:
        print(f"Error generating the dataset: {e}")
        return None
