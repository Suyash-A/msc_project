#!/bin/bash

# Define paths
PYTHON_SCRIPT="../src/data/generate_input_chexbert.py"
REPORTS_PATH="../data_msc_project/physionet.org/files/mimic-cxr/2.0.0"
OUTPUT_PATH="../data_msc_project/cheXbert"
STUDY_LIST_PATH="../data_msc_project/eval_set/test-set-destinations.csv"

# Run the Python script with the specified arguments and the --no_split option
python $PYTHON_SCRIPT --reports_path $REPORTS_PATH --output_path $OUTPUT_PATH --no_split --study_list $STUDY_LIST_PATH

echo "Script execution completed. Output saved to $OUTPUT_PATH."

