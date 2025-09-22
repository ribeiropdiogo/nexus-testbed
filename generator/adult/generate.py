"""
Script to generate the adult dataset from the source data.
"""

import os
import json
import random

INPUT = "adult.data"
DBENTRIES = 10
DBFIELDS  = 6
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

def age_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = int(row[0])
    # Initialize the object for age
    obj = {
        "name": "age_" + str(rowId),
        "datatype": "continuous",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            # Introduce noise by adding or subtracting a random value
            noise_value = random.randint(-20, 20)
            while noise_value == 0:
                noise_value = random.randint(-20, 20)
            value = max(0, truth + noise_value)
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

def education_entry(dataset, row, rowId, noise, sources):
    # Initialize list of possible education values
    education_values = [
        'Bachelors', 'Some-college', '11th', 'HS-grad', 
        'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', 
        '7th-8th', '12th', 'Masters', '1st-4th', '10th', 
        'Doctorate', '5th-6th', 'Preschool'
    ]
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = row[3]
    # Initialize the object
    obj = {
        "name": "education_" + str(rowId),
        "datatype": "categorical",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            value = random.choice(education_values)
            while value == truth:
                value = random.choice(education_values)
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

def workclass_entry(dataset, row, rowId, noise, sources):
    # Initialize list of possible workclass values
    workclass_values = [
        'Private', 'Self-emp-not-inc', 'Self-emp-inc',
        'Federal-gov', 'Local-gov', 'State-gov', 
        'Without-pay', 'Never-worked'
    ]
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = row[1]
    # Initialize the object for workclass
    obj = {
        "name": "workclass_" + str(rowId),
        "datatype": "categorical",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            value = random.choice(workclass_values)
            while value == truth:
                value = random.choice(workclass_values)
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

def marital_entry(dataset, row, rowId, noise, sources):
    # List of possible marital status values
    marital_values = [
        'Married-civ-spouse', 'Divorced', 'Never-married', 
        'Separated', 'Widowed', 'Married-spouse-absent', 
        'Married-AF-spouse'
    ]
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = row[5]
    # Initialize the object
    obj = {
        "name": "marital_" + str(rowId),
        "datatype": "categorical",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            value = random.choice(marital_values)
            while value == truth:
                value = random.choice(marital_values)
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

def country_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = row[13]
    # Initialize the object
    obj = {
        "name": "country" + str(rowId),
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

def hours_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = int(row[12])
    # Initialize the object for hours-per-week
    obj = {
        "name": "hours_" + str(rowId),
        "datatype": "continuous",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            # Introduce noise by adding or subtracting a random value
            noise_value = random.randint(-20, 20)
            while noise_value == 0:
                noise_value = random.randint(-20, 20)
            value = max(0, truth + noise_value)
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
        # Open the data file and read line by line
        with open("generator/adult/" + INPUT, "r", encoding="utf-8") as file:
            data = []
            for line in file:
                # Remove whitespace and split by comma
                fields = [f.strip() for f in line.strip().split(",")]
                # Skip empty lines
                if not fields or len(fields) < 1 or fields[0] == '':
                    continue
                data.append(fields)
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
                age_entry(dataset, row, rowId, noise, sources)
                workclass_entry(dataset, row, rowId, noise, sources)
                marital_entry(dataset, row, rowId, noise, sources)
                education_entry(dataset, row, rowId, noise, sources)
                country_entry(dataset, row, rowId, noise, sources)
                hours_entry(dataset, row, rowId, noise, sources)
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
