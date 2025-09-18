"""
Script to generate the diabetes dataset from the source data.
"""

import os
import json
import csv
import random

INPUT = "winequality-red.csv"
DBENTRIES = 10


def process_entry(dataset, row, rowId, noise, sources):
    # Iterate over row columns
    for col in row:
        # Initialize the noise counter
        noisy_sources = noise
        # Set the truth value
        truth = float(row[col])
        # Initialize the object for diabetes
        obj = {
            "name": col + "_" + str(rowId),
            "datatype": "continuous",
            "truth": truth,
            "claims": []
        }
        # Iterate over the number of sources
        for i in range(sources):
            if noisy_sources > 0:
                # Introduce noise
                multiplier = random.uniform(0.1, 2.0)
                # Check if multiplier is not 1
                while multiplier == 1.0:
                    multiplier = random.uniform(0.1, 2.0)
                if truth == 0:
                    # Sum multiplier to truth value
                    value = round(truth + multiplier, 2)
                else:
                    # Apply multiplier to truth value
                    value = round(truth * multiplier, 2)
                noisy_sources -= 1
            else:
                value = truth
            # Create entry object
            entry = {
                "sourceId": f"source{i+1}",
                "fact": float(value)
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
        with open("generator/wine/" + INPUT, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, quotechar='"', delimiter=';')
            data = list(reader)
            if len(data) > DBENTRIES:
                data = data[:DBENTRIES]
            # Get number of claims
            claims = len(data[0]) * len(data) * sources
            print(f"\n > Number of individual claims: {claims}")
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
                process_entry(dataset, row, rowId, noise, sources)
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
