"""
This module contains the code responsible for the nexus algorithm
to perform the tests and assess the results.
"""

import random
import sys
import json
import os
import copy
import requests

from metrics import calculate_metrics

HEADERS = {'Content-type': 'application/json'}

def assess(dataset, output, datatype, output_file):
    """
    Consume the input dataset file and use Nexus.
    """
    # Clear data
    r = requests.get(
        'http://127.0.0.1:8000/clear',
        headers=HEADERS,
        timeout=3600
    )
    # Read input file
    with open(dataset, "r", encoding="utf-8") as file:
        # Load JSON data
        data = json.load(file)
        # Shuffke the objects
        random.shuffle(data['objects'])
        # Shuffle the claims
        for obj in data['objects']:
            random.shuffle(obj['claims'])
        # Auxiliary variable
        k = 1
        # Create directory if it does not exist
        datatype = datatype.replace("./datasets/", "")[:-1]
        nexus_path = output_file.replace(f"{datatype}/nexus", f"nexus/{datatype}")
        os.makedirs(os.path.dirname(nexus_path), exist_ok=True)
        # Iterate over the objects and claims
        for obj in data['objects']:
            # Iterate claims to consolidate sequentially
            for i in range(len(obj['claims'])):
                # Make a copy of the data
                sequential_data = copy.deepcopy(data)
                # Crop the claims foreach object
                for j in range(len(sequential_data['objects'])):
                    sequential_data['objects'][j]['claims'] = sequential_data['objects'][j]['claims'][:i+1]
                # Perform request
                r = requests.post(
                    'http://127.0.0.1:8000/consolidate',
                    data=json.dumps(sequential_data),
                    headers=HEADERS,
                    timeout=3600
                )
                # Load the response
                result = json.loads(r.text)
                # Create result path
                result_path = nexus_path.replace(".json", f"_{k}_{i+1}.json")
                # Save the response to a file
                with open(result_path, "w", encoding="utf-8") as resp_file:
                    json.dump(result, resp_file, indent=4)
            # Increment k
            k += 1
        # Iterate over the objects in the result
        for obj in result['objects']:
            # Iterate over the objects in the data
            for entry in data['objects']:
                # Get the matching entry
                if entry['name'] == obj['name']:
                    # Create a result object
                    robj = {
                        "result": str(obj['claims'][0]['fact']),
                        "truth": str(entry['truth']),
                        "datatype": entry['datatype']
                    }
                    # Calculate distances
                    robj['metrics'] = calculate_metrics(robj)
                    # Append result to output
                    output['results'].append(robj)

if __name__ == "__main__":
    # Initialize json object
    output = {
        "algorithm": "Nexus",
        "results": [],
    }
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        # Extract command line arguments
        datatype    = sys.argv[1]
        input_file  = sys.argv[2]
        output_file = sys.argv[3]
        # Perform assessment
        assess(input_file, output, datatype, output_file)
        # Write output to file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)
    else:
        # Print usage message
        print("Usage: python nexus.py <datatype> <input_file> <output_file>")
        print("Example: python nexus.py testbed truth/gold.txt output.json")
        sys.exit(1)