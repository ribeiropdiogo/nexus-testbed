import csv

# Input CSV file name
input_csv = "../csv/heterogeneous.csv"

# Output .dat file name
output_dat = "./boxplot/heterogeneous.dat"

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

data = []

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        values = []
        for col in columns_to_average:
            val = row[col]
            if val != "":
                values.append(float(val))
        avg_accuracy = sum(values) / len(values) if values else 0
        data.append((row['algorithm'], avg_accuracy))

# Sort by algorithm name
data.sort(key=lambda x: x[0])

with open(output_dat, 'w', encoding='utf-8') as outfile:
    outfile.write("Algorithm Accuracy\n")
    for alg, avg in data:
        outfile.write(f"{alg} {avg:.6f}\n")

print(f"Output written to {output_dat}")
