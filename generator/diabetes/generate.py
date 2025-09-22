"""
Script to generate the diabetes dataset from the source data.
"""

from operator import add
import os
import json
import csv
import random

INPUT = "diabetes_binary_health_indicators_BRFSS2015.csv"
DBENTRIES = 50
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

def diabetes_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = "yes" if row['Diabetes_binary'] == "1.0" else "no"
    # Initialize the object for diabetes
    obj = {
        "name": "diabetes_" + str(rowId),
        "datatype": "categorical",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            if truth == "yes":
                value = "no"
            else:
                value = "yes"
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

def highbp_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = "high BP" if row['HighBP'] == "1.0" else "no high BP"
    # Initialize the object
    obj = {
        "name": "highbp_" + str(rowId),
        "datatype": "categorical",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            if truth == "high BP":
                value = "no high BP"
            else:
                value = "high BP"
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

def highchol_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = "high cholesterol" if row['HighChol'] == "1.0" else "no high cholesterol"
    # Initialize the object
    obj = {
        "name": "highchol_" + str(rowId),
        "datatype": "categorical",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            if truth == "high cholesterol":
                value = "no high cholesterol"
            else:
                value = "high cholesterol"
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

def bmi_entry(dataset, row, rowId, noise, sources):
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = float(row['BMI'])
    # Initialize the object
    obj = {
        "name": "bmi_" + str(rowId),
        "datatype": "continuous",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            value = float(truth) + random.choices([3,4,5,-3,-4,-5], k=1)[0]
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

def age_entry(dataset, row, rowId, noise, sources):
    # Initialize a dict that maps an int to a string
    age_map = {
        1.0: "18-24",
        2.0: "25-29",
        3.0: "30-34",
        4.0: "35-39",
        5.0: "40-44",
        6.0: "45-49",
        7.0: "50-54",
        8.0: "55-59",
        9.0: "60-64",
        10.0: "65-69",
        11.0: "70-74",
        12.0: "75-79",
        13.0: "80 or older"
    }
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = age_map.get(float(row['Age']))
    # Initialize the object
    obj = {
        "name": "age_" + str(rowId),
        "datatype": "categorical",
        "truth": truth,
        "claims": []
    }
    # Iterate over the number of sources
    for i in range(sources):
        if noisy_sources > 0:
            value = random.choice(list(age_map.values()))
            while value == truth:
                value = random.choice(list(age_map.values()))
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
    # Initialize a dict that maps an int to a string
    education_map = {
        1.0: "Never attended school or only kindergarten",
        2.0: "Grades 1 through 8 (Elementary)",
        3.0: "Grades 9 through 11 (Some high school)",
        4.0: "Grade 12 or GED (High school graduate)",
        5.0: "College 1 year to 3 years (Some college or technical school)",
        6.0: "College 4 years or more (College graduate)"
    }
    # Initialize the noise counter
    noisy_sources = noise
    # Set the truth value
    truth = education_map.get(float(row['Education']))
    # Initialize the object
    obj = {
        "name": "education_" + str(rowId),
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

def generate(noise: int, sources: int, output_path: str):
    """
    Open the source data and generate the dataset.
    """
    try:
        # Open the csv file
        with open("generator/diabetes/" + INPUT, "r", encoding="utf-8") as file:
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
                diabetes_entry(dataset, row, rowId, noise, sources)
                highbp_entry(dataset, row, rowId, noise, sources)
                highchol_entry(dataset, row, rowId, noise, sources)
                bmi_entry(dataset, row, rowId, noise, sources)
                age_entry(dataset, row, rowId, noise, sources)
                education_entry(dataset, row, rowId, noise, sources)
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
