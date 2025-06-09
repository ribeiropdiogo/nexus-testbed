#!/bin/bash

# Promp user for which segments to run
read -p "Do you want to run the dataset generation? (yes/no): " run_dataset

# Check response
if [[ "$run_dataset" == "yes" ]]; then
    ./generator.sh
elif [[ "$run_dataset" == "no" ]]; then
    echo "Skipping dataset generation."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi