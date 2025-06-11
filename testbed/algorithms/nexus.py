"""
This module contains the code responsible for the nexus algorithm
to perform the tests and assess the results.
"""

import sys
import json
import time
import requests

from metrics import calculate_metrics

HEADERS = {'Content-type': 'application/json'}

def assess(dataset, output):
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
        # Perform request
        r = requests.post(
            'http://127.0.0.1:8000/consolidate',
            data=json.dumps(data),
            headers=HEADERS,
            timeout=3600
        )
        # Load the response
        result = json.loads(r.text)
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
        assess(input_file, output)
        # Write output to file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)
    else:
        # Print usage message
        print("Usage: python nexus.py <datatype> <input_file> <output_file>")
        print("Example: python nexus.py testbed truth/gold.txt output.json")
        sys.exit(1)