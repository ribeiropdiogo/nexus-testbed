"""
This module contains the code responsible for the nexus algorithm
to perform the tests and assess the results.
"""

import random
import sys
import json
import os
import requests

from metrics import calculate_metrics

HEADERS = {'Content-type': 'application/json'}

def assess(path, file, round):
    """
    Consume the input file and use Nexus.
    """
    # Read input file
    with open(os.path.join(path, file), "r", encoding="utf-8") as file:
        # Load JSON data
        data = json.load(file)
        # Shuffle the objects
        random.shuffle(data['objects'])
        # Shuffle the claims
        for obj in data['objects']:
            random.shuffle(obj['claims'])
        if 'gender' in path:
            port = 8001
        elif 'adult' in path:
            port = 8002
        elif 'diabetes' in path:
            port = 8003
        else:
            sys.exit(1)
        print(path)
        print(port)
        sys.exit(1)
        # Perform request
        r = requests.post(
            f'http://127.0.0.1:{port}/consolidate',
            data=json.dumps(data),
            headers=HEADERS,
            timeout=3600
        )
        # Load the response
        result = json.loads(r.text)
        # Build output path
        output_path   = f"{file.name}".replace("datasets-real", "results-real")
        output_path   = output_path.replace("subject", f"/{round}/subject")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Save the response to a file
        with open(output_path, "w", encoding="utf-8") as resp_file:
            json.dump(result, resp_file, indent=4)
        # Initialize json object
        output = {
            "algorithm": "Nexus",
            "results": [],
        }
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
        
        # Write output to file
        output_path = output_path.replace("subject", "metrics/subject")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)


if __name__ == "__main__":
    # Clear data
    r = requests.get(
        'http://127.0.0.1:8000/clear',
        headers=HEADERS,
        timeout=3600
    )
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        # Extract command line arguments
        datatype     = sys.argv[1]
        input_folder = sys.argv[2]
        output_file  = sys.argv[3]
        round        = sys.argv[4]
        # Build dataset path
        path = f"{datatype}{input_folder}/"
        # Collect files in the dataset folder
        files = os.listdir(path)
        # Shuffle files
        random.shuffle(files)
        # Initialize k
        k = 1
        # Iterate over files
        for file in files:
            # Perform assessment
            assess(path, file, round)
    else:
        # Print usage message
        print("Usage: python nexus.py <datatype> <input_folder>")
        print("Example: python nexus.py wine ./datasets-real/wine/")
        sys.exit(1)