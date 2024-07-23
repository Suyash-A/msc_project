#!/bin/bash

# Define paths
PYTHON_SCRIPT="../src/evaluation/eval_chexpert.py"
TRUE_LABELS="../data_msc_project/physionet.org/files/mimic-cxr-jpg/2.1.0/mimic-cxr-2.1.0-test-set-labeled.csv"
PRED_LABELS_DIR="../data_msc_project/cheXpert"
ORDERED_TEST_IDS="../data_msc_project/eval_set/ordered_test_ids.csv"

# Run the Python script with the specified arguments
python $PYTHON_SCRIPT --true_labels $TRUE_LABELS --pred_labels_dir $PRED_LABELS_DIR --ordered_test_ids $ORDERED_TEST_IDS

echo "F1 score computation completed."
