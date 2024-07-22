#!/bin/bash

# Define paths
PYTHON_SCRIPT="../src/data/test_set_destinations.py"
LABELED_FILE="../data_msc_project/physionet.org/files/mimic-cxr-jpg/2.1.0/mimic-cxr-2.1.0-test-set-labeled.csv"
STUDY_LIST_FILE="../data_msc_project/physionet.org/files/mimic-cxr/2.0.0/cxr-study-list.csv"
OUTPUT_FILE="../data_msc_project/eval_set/test-set-destinations.csv"

# Run the Python script with the specified arguments
python $PYTHON_SCRIPT --labeled_file $LABELED_FILE --study_list_file $STUDY_LIST_FILE --output_file $OUTPUT_FILE

echo "Script execution completed. Output saved to $OUTPUT_FILE."

