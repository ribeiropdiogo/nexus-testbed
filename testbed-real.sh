#!/bin/bash

# List of possible algorithms
# Possible algorithms to run: nexus
ALGORITHMS=("nexus")
# Number of executions
ROUNDS=5

echo "============================================================="
echo "                Testbed Execution (real)                     "
echo "============================================================="

# Prompt user for which directory to use
read -p "Do you want to use the default directory (datasets-real/)? [Y/n]: " use_default

if [[ "$use_default" =~ ^([Nn][Oo]?|[Nn])$ ]]; then
    read -p "Please enter the directory to use: " custom_dir
    dir="./$custom_dir/"
else
    dir="./datasets-real/"
fi

echo "Running testbed.sh using files in $dir directory..."

# Prompt user if it wants to run the tests
read -p "Do you want to run the tests? [Y/n]: " run_tests
if [[ "$run_tests" =~ ^([Yy][Ee][Ss]?|[Yy])$ ]]; then
    start=$(date +%s)
    # Iterate through each folder in the directory
    for folder in "$dir"*/; do
        [ -d "$folder" ] || continue
        echo "> Performing tests for $(basename "$folder") data..."
        # Build output directory
        output_dir="${folder/datasets/results}"
        # Iterate through each algorithm
        for algorithm in "${ALGORITHMS[@]}"; do
            echo "    > Performing tests for $algorithm..."
            # Iterate the subfolders in the folder
            for subfolder in "$folder"*/; do
                [ -d "$subfolder" ] || continue
                    folder_basename="$(basename "$subfolder")"
                    echo "        > Performing tests for $folder_basename..."
                    # Create the output directory if it doesn't exist
                    mkdir -p "${output_dir}${folder_basename}/"
                    # Iterate for ROUNDS rounds
                    for ((i=1; i<=ROUNDS; i++))
                    do
                        # Build output file name
                        base_name="$(basename "$file" .json)"
                        output_file="${output_dir}${base_name}${folder_basename}_${i}.json"
                        # Create the output directory if it doesn't exist
                        mkdir -p "${output_dir}/"
                        python3 testbed-real/nexus.py $folder $folder_basename $output_file $i
                    done
            done
        done
    done
    end=$(date +%s)
    echo "Elapsed time: $(( end - start )) seconds"
else
    echo "Skipping tests."
fi

# Prompt user if it wants to calculate statistics
read -p "Do you want to calculate statistics for the results? [Y/n]: " calc_stats
if [[ "$calc_stats" =~ ^([Nn][Oo]?|[Nn])$ ]]; then
    echo "Skipping statistics calculation."
    exit 0
fi

echo "Calculating statistics for the results..."

# Iterate through each folder in the directory
for folder in "$dir"*/; do
    [ -d "$folder" ] || continue
    echo "> Calculating statistics for $(basename "$folder") results..."
    # Build output directory
    output_dir="${folder/datasets/results}"
    # Iterate output dir
    for subfolder in "$output_dir"*/; do
        [ -d "$subfolder" ] || continue
        # Iterate the files in the output_dir
        echo "    > Processing files in $subfolder"
        # Run the statistics script
        python3 testbed-real/stats.py $(basename "$folder") $subfolder
    done
    # Run the summary script
    echo "> Generating csv summary for $(basename "$folder")..."
    #python3 testbed-synthetic/summary.py $(basename "$folder")
done

                