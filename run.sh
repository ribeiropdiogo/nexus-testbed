#!/bin/bash

# Prompt user if it wants to clean data
read -p "Do you want to clean data? (yes/no): " clean_data
# Check response
if [[ "$clean_data" == "yes" || "$clean_data" == "y" ]]; then
    # Prompt user if it wants to clean the datasets directory
    read -p "Do you want to clean the datasets/ directory? (yes/no): " clean_datasets
    # Check response
    if [[ "$clean_datasets" == "yes" || "$clean_datasets" == "y" ]]; then
        echo "Cleaning datasets/ directory..."
        rm -rf datasets/*
    elif [[ "$clean_datasets" == "no" || "$clean_datasets" == "n" ]]; then
        echo "Skipping datasets/ directory cleaning."
    else
        echo "Error: Invalid input. Please answer with 'yes' or 'no'."
        exit 1
    fi
    # Prompt user if it wants to clean the results directory
    read -p "Do you want to clean the results/ directory? (yes/no): " clean_results
    # Check response
    if [[ "$clean_results" == "yes" || "$clean_results" == "y" ]]; then
        echo "Cleaning results/ directory..."
        rm -rf results/*
    elif [[ "$clean_results" == "no" || "$clean_results" == "n" ]]; then
        echo "Skipping results/ directory cleaning."
    else
        echo "Error: Invalid input. Please answer with 'yes' or 'no'."
        exit 1
    fi
    # Prompt user if it wants to clean the stats directory
    read -p "Do you want to clean the stats/ directory? (yes/no): " clean_stats
    # Check response
    if [[ "$clean_stats" == "yes" || "$clean_stats" == "y" ]]; then
        echo "Cleaning stats/ directory..."
        rm -rf stats/*
    elif [[ "$clean_stats" == "no" || "$clean_stats" == "n" ]]; then
        echo "Skipping stats/ directory cleaning."
    else
        echo "Error: Invalid input. Please answer with 'yes' or 'no'."
        exit 1
    fi
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