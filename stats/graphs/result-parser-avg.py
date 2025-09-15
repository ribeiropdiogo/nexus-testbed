import csv

# Input CSV file name
input_csv = "../csv/categorical.csv"

# Columns to average (header names)
columns_to_average = [
    "direct comparison",
    #"euclidean",
    #"manhattan",
    #"canberra",
    #"jaro-winkler",
    #"sorensen-dice",
    #"damerau-levenshtein"
]

# Initialize algorithms
data = {
    'truthfinder': 0,
    'crh': 0,
    'nexus': 0
}

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    ROWS = 0
    for row in reader:
        values = []
        for col in columns_to_average:
            val = row[col]
            if val != "":
                data[row['algorithm']] += float(val)
            else:
                print(f"Warning: Empty value found in row {row['algorithm']} for column {col}")
        ROWS += 1
    print(f"Total rows processed: {ROWS}")
    print("#"* 20)
    print("Sums:")
    for algorithm, sum in data.items():
        print(f"{algorithm}: {sum:.4f}")
    print("#"* 20)
    # Calculate average for each algorithm
    for algorithm in data:
        if ROWS > 0:
            data[algorithm] /= (ROWS/3) * len(columns_to_average)
    print("Averages:")
    for algorithm, avg in data.items():
        print(f"{algorithm}: {avg:.4f}")
    print("#"* 20)
