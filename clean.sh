#!/bin/bash

# Prompt user if it wants to clean the datasets directory
read -p "Do you want to clean the datasets/ directory? (yes/no): " clean_datasets
# Check response
if [[ "$clean_datasets" == "yes" || "$clean_datasets" == "y" ]]; then
    echo "Cleaning datasets/ directory..."
    rm -rf datasets/*
    touch datasets/.gitkeep  # Keep the .gitkeep file if it exists
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
    touch results/.gitkeep  # Keep the .gitkeep file if it exists
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
    touch stats/.gitkeep  # Keep the .gitkeep file if it exists
elif [[ "$clean_stats" == "no" || "$clean_stats" == "n" ]]; then
    echo "Skipping stats/ directory cleaning."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi
