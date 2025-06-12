#!/bin/bash

# Prompt user if it wants to clean data
read -p "Do you want to clean data? (yes/no): " clean_data
# Check response
if [[ "$clean_data" == "yes" || "$clean_data" == "y" ]]; then
    ./clean.sh
elif [[ "$clean_data" == "no" || "$clean_data" == "n" ]]; then
    echo "Skipping data cleaning."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi

# Promp user for dataset generation
read -p "Do you want to run the dataset generation? (yes/no): " run_dataset
# Check response
if [[ "$run_dataset" == "yes" || "$run_dataset" == "y" ]]; then
    ./generator.sh
elif [[ "$run_dataset" == "no" || "$run_dataset" == "n" ]]; then
    echo "Skipping dataset generation."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi

# Prompt user for test execution
read -p "Do you want to run the tests? (yes/no): " run_tests
# Check response
if [[ "$run_tests" == "yes" || "$run_tests" == "y" ]]; then
    ./testbed.sh
elif [[ "$run_tests" == "no" || "$run_tests" == "n" ]]; then
    echo "Skipping tests."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi