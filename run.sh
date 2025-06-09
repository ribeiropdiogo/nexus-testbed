#!/bin/bash

# Promp user for which segments to run
read -p "Do you want to run the dataset generation? (yes/no): " run_dataset

# Check response
if [[ "$run_dataset" == "yes" ]]; then
    echo "================================================="
    echo "         Dataset Generation Parameters           "
    echo "================================================="

    # Prompt execution mode
    read -p "Do you want to run the preset generator? (yes/no): " run_preset
    if [[ "$run_preset" == "yes" ]]; then

        for datatype in string continuous categorical heterogeneous; do
            for sources in 5 10 15 20; do
                for noise in 0.0 0.2 0.4 0.6 0.9; do
                    echo "================================================="
                    python3 generator/generator.py --datatype "$datatype" --sources "$sources" --noise "$noise"
                done
            done
        done
        exit 0
    elif [[ "$run_preset" == "no" ]]; then
        # Prompt argument
        read -p "Enter datatype: " datatype
        # Validate input
        if [[ "$datatype" != "string" && "$datatype" != "continuous" && "$datatype" != "categorical" && "$datatype" != "heterogeneous" ]]; then
            echo "Error: datatype must be one of: string, continuous, categorical, heterogeneous."
            exit 1
        fi

        # Prompt argument
        read -p "Enter sources: " sources
        # Validate input
        if ! [[ "$sources" =~ ^[0-9]+$ ]]; then
            echo "Error: sources must be an integer."
            exit 1
        fi

        # Prompt argument
        read -p "Enter noise: " noise
        # Validate input
        if ! [[ "$noise" =~ ^([0-9]*\.?[0-9]+)$ ]] || (( $(echo "$noise < 0.0" | bc -l) )) || (( $(echo "$noise > 1.0" | bc -l) )); then
            echo "Error: noise must be a number between 0.0 and 1.0."
            exit 1
        fi

        echo "================================================="

        python3 generator/generator.py --datatype "$datatype" --sources "$sources" --noise "$noise"

        exit 0
    else
        echo "Error: Invalid input. Please answer with 'yes' or 'no'."
        exit 1
    fi
elif [[ "$run_dataset" == "no" ]]; then
    echo "Skipping dataset generation."
else
    echo "Error: Invalid input. Please answer with 'yes' or 'no'."
    exit 1
fi