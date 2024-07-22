#!/bin/bash

# Check if the number of runs is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <number_of_runs>"
    exit 1
fi

# Define paths
CHEXBERT_PATH="../models/CheXbert/src"
INPUT_PATH="../data_msc_project/cheXbert/input_chexbert.csv"
OUTPUT_PATH="../data_msc_project/cheXbert"
MODEL_PATH="../models/CheXbert/model_path/chexbert.pth"

# Get the number of runs from the command-line argument
NUM_RUNS=$1

# Run the CheXbert labeler the specified number of times
for ((i=1; i<=NUM_RUNS; i++))
do
    OUTPUT_FILE="${OUTPUT_PATH}/chexbert_labeled_${i}.csv"
    python $CHEXBERT_PATH/label.py -d=$INPUT_PATH -o=$OUTPUT_FILE -c=$MODEL_PATH
    echo "Run $i completed. Output saved to $OUTPUT_FILE."
done

echo "All runs completed."

