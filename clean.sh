#!/bin/bash

# Read the first argumento into a variable
type=$1

# Prompt user if it wants to clean the datasets directory
read -p "Do you want to clean the datasets-$type/ directory? (yes/no): " clean_datasets
# Check response
if [[ "$clean_datasets" == "yes" || "$clean_datasets" == "y" ]]; then
    echo "Cleaning datasets-$type/ directory..."
    rm -rf datasets-$type/*
    touch datasets-$type/.gitkeep  # Keep the .gitkeep file if it exists
elif [[ "$clean_datasets" == "no" || "$clean_datasets" == "n" ]]; then
    echo "Skipping datasets-$type/ directory cleaning."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi
# Prompt user if it wants to clean the results directory
read -p "Do you want to clean the results-$type/ directory? (yes/no): " clean_results
# Check response
if [[ "$clean_results" == "yes" || "$clean_results" == "y" ]]; then
    echo "Cleaning results-$type/ directory..."
    rm -rf results-$type/*
    touch results-$type/.gitkeep  # Keep the .gitkeep file if it exists
elif [[ "$clean_results" == "no" || "$clean_results" == "n" ]]; then
    echo "Skipping results-$type/ directory cleaning."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi
# Prompt user if it wants to clean the stats directory
read -p "Do you want to clean the stats-$type/ directory? (yes/no): " clean_stats
# Check response
if [[ "$clean_stats" == "yes" || "$clean_stats" == "y" ]]; then
    echo "Cleaning stats-$type/ directory..."
    rm -rf stats-$type/*
    touch stats-$type/.gitkeep  # Keep the .gitkeep file if it exists
elif [[ "$clean_stats" == "no" || "$clean_stats" == "n" ]]; then
    echo "Skipping stats-$type/ directory cleaning."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi
