import os
import json
import math



# Input CSV file name
input_dir = "../../results/heterogeneous/nexus"


noise = {
    '20': ['s5_n1', 's10_n2', 's15_n3', 's20_n4'],
    '40': ['s5_n2', 's10_n4', 's15_n6', 's20_n8'],
    '60': ['s5_n3', 's10_n6', 's15_n9', 's20_n12'],
    '80': ['s10_n8', 's15_n12', 's20_n16']
}

for key, value in noise.items():
    correct = 0
    incorrect = 0

    print(f"{key}% noise:")
    
    json_files = [
        f for f in os.listdir(input_dir)
        if f.endswith('.json') and any(f.startswith(prefix) for prefix in value)
    ]

    for filename in json_files:
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)


            for entry in data['results']:
                if entry['datatype'] == 'continuous':
                    if float(entry['truth']) == math.floor(float(entry['result'])):
                        correct += 1
                    else:
                        incorrect += 1
                else:
                    if entry['truth'] == entry['result']:
                        correct += 1
                    else:
                        incorrect += 1

    print(f"Correct: {correct}, Incorrect: {incorrect}")
    total = correct + incorrect
    percent_incorrect = (incorrect / total) * 100
    print(f"Incorrect Percentage: {percent_incorrect:.2f}%")
