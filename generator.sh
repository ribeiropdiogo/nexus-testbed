#!/bin/bash

echo "================================================="
echo "         Dataset Generation Parameters           "
echo "================================================="


# Prompt for synthetic or real-world dataset
read -p "Do you want to generate a synthetic or real-world dataset? (s/r): " dataset_type
if [[ "$dataset_type" != "s" && "$dataset_type" != "r" ]]; then
    echo "Error: Please answer with 's' or 'r'."
    exit 1
fi

# If synthetic, run generator-synthetic.py
if [[ "$dataset_type" == "s" ]]; then
    # Prompt execution mode
    read -p "Do you want to run the preset generator? (yes/no): " run_preset
    if [[ "$run_preset" == "yes" || "$run_preset" == "y" ]]; then

        for datatype in string continuous categorical heterogeneous; do
            for sources in 5 10 15 20; do
                for noise in 0.2 0.4 0.6 0.8; do
                    echo "================================================="
                    python3 generator/generator-synthetic.py --datatype "$datatype" --sources "$sources" --noise "$noise"
                done
            done
        done
        exit 0
    elif [[ "$run_preset" == "no" || "$run_preset" == "n" ]]; then
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
# If real-world, run generator-real.py
else
    # Prompt which dataset to generate
    read -p "Which real-world dataset do you want to generate? (diabetes -> d | adult -> a | gender -> g): " real_dataset
    if [[ "$real_dataset" == "d" ]]; then
        datatype="diabetes"
    elif [[ "$real_dataset" == "a" ]]; then
        datatype="adult"
    elif [[ "$real_dataset" == "g" ]]; then
        datatype="gender"
    else
        echo "Error: Invalid input. Please answer with 'd', 'w', or 'a'."
        exit 1
    fi
    # Prompt number of sources
    read -p "Enter number of sources: " sources
    if ! [[ "$sources" =~ ^[0-9]+$ ]]; then
        echo "Error: sources must be an integer."
        exit 1
    fi
    # Prompt noise level(s)
    read -p "Enter noise level(s) (single float or space/comma-separated list, 0.0 to 1.0): " noise_input

    # Normalize input: replace commas with spaces
    noise_input="${noise_input//,/ }"
    # Split into array
    read -ra noise_arr <<< "$noise_input"

    # Validate and run for each noise value
    for noise in "${noise_arr[@]}"; do
        if ! [[ "$noise" =~ ^([0-9]*\.?[0-9]+)$ ]] || (( $(echo "$noise < 0.0" | bc -l) )) || (( $(echo "$noise > 1.0" | bc -l) )); then
            echo "Error: each noise value must be a number between 0.0 and 1.0."
            exit 1
        fi
        echo "================================================="
        python3 generator/generator-real.py --datatype "$datatype" --sources "$sources" --noise "$noise"
    done
    exit 0
fi