#!/bin/bash
echo "================================================="
echo "         Dataset Generation Parameters           "
echo "================================================="

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
read -p "Enter claims: " claims
# Validate input
if ! [[ "$claims" =~ ^[0-9]+$ ]]; then
    echo "Error: claims must be an integer."
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

python3 generator/generator.py --datatype "$datatype" --sources "$sources" --claims "$claims" --noise "$noise"