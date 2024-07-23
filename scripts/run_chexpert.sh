#!/bin/bash

# Check if the number of runs is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <number_of_runs>"
    exit 1
fi

# Define paths
CHEXPERT_PATH="../models/chexpert-labeler"
REPORT_PATH="../data_msc_project/cheXpert/input_chexpert.csv"
OUTPUT_PATH="../data_msc_project/cheXpert"

# Get the number of runs from the command-line argument
NUM_RUNS=$1

# Run the CheXpert labeler the specified number of times
for ((i=1; i<=NUM_RUNS; i++))
do
    OUTPUT_FILE="${OUTPUT_PATH}/chexpert_labeled_${i}.csv"
    python $CHEXPERT_PATH/label.py --verbose --reports_path $REPORT_PATH --output_path $OUTPUT_FILE --mention_phrases_dir $CHEXPERT_PATH/phrases/mention --unmention_phrases_dir $CHEXPERT_PATH/phrases/unmention --pre_negation_uncertainty_path $CHEXPERT_PATH/patterns/pre_negation_uncertainty.txt --negation_path $CHEXPERT_PATH/patterns/negation.txt --post_negation_uncertainty_path $CHEXPERT_PATH/patterns/post_negation_uncertainty.txt
    echo "Run $i completed. Output saved to $OUTPUT_FILE."
done

echo "All runs completed."

