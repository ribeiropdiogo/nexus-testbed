"""
Reference implementation of the Majority Voting algorithm.
"""

import json
import sys
import random
from collections import Counter

import textdistance as td

from metrics import calculate_metrics

INPUT_FILE = "truth/gold.txt"

def voting(claims):
    """
    Majority Voting algorithm implementation.
    """
    facts = []
    # Extract facts
    for entry in claims:
        facts.append(entry['fact'])
    # Get the most common fact (majority)
    counter = Counter(facts)
    majority = counter.most_common(1)[0][0]
    # Return value
    return majority

def assess(dataset, output):
    """
    Consume the input dataset file and perform majority voting.
    """
    # Read input file
    with open(dataset, "r", encoding="utf-8") as file:
        # Load JSON data
        data = json.load(file)
        # Iterate through objects
        for obj in data['objects']:
            # Extract claims
            claims = obj['claims']
            # Shuffle claims to ensure randomness
            random.shuffle(claims)
            # Perform voting
            result = voting(claims)
            # Create a result object
            data = {
                "result": result,
                "truth": obj['truth'],
                "datatype": obj['datatype']
            }
            # Calculate distances
            data['metrics'] = calculate_metrics(data)
            # Append result to output
            output['results'].append(data)

if __name__ == "__main__":
    # Initialize json object
    output = {
        "algorithm": "Majority Voting",
        "results": [],
    }
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        # Extract command line arguments
        datatype    = sys.argv[1]
        input_file  = sys.argv[2]
        output_file = sys.argv[3]
        # Perform assessment
        assess(input_file, output)
        # Write output to file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)
    else:
        # Print usage message
        print("Usage: python majority.py <datatype> <input_file> <output_file>")
        print("Example: python majority.py testbed truth/gold.txt output.json")
        sys.exit(1)
