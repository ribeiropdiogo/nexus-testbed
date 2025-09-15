import csv
import pprint
from collections import defaultdict

# Input CSV file name
input_csv = "../csv/heterogeneous.csv"

# Columns to average (header names)
columns_to_average = [
    "direct comparison",
    "euclidean",
    "manhattan",
    "canberra",
    "jaro-winkler",
    "sorensen-dice",
    "damerau-levenshtein"
]

# Initialize algorithms
data = {
    'truthfinder': {},
    'crh': {},
    'nexus': {}
}

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    ROWS = 0
    for row in reader:
        values = []
        algorithm = row['algorithm']
        test = row['test']
        for col in columns_to_average:
            if test not in data[algorithm]:
                data[algorithm][test] = 0.0
            data[algorithm][test] += (float(row[col])/len(columns_to_average)) if row[col] else 0.0

    pprint.pprint(data)

    print("#"* 20)
    print("20% noise:")
    for algorithm, tests in data.items():
        v = tests['s5_n1'] + tests['s10_n2'] + tests['s15_n3'] + tests['s20_n4']
        v /= 4
        print(f"{algorithm}: {v:.4f}")
    print("40% noise:")
    for algorithm, tests in data.items():
        v = tests['s5_n2'] + tests['s10_n4'] + tests['s15_n6'] + tests['s20_n8']
        v /= 4
        print(f"{algorithm}: {v:.4f}")
    print("60% noise:")
    for algorithm, tests in data.items():
        v = tests['s5_n3'] + tests['s10_n6'] + tests['s15_n9'] + tests['s20_n12']
        v /= 4
        print(f"{algorithm}: {v:.4f}")
    print("80% noise:")
    for algorithm, tests in data.items():
        v = tests['s10_n8'] + tests['s15_n12'] + tests['s20_n16']
        v /= 3
        print(f"{algorithm}: {v:.4f}")