#!/bin/bash

# Define paths
PYTHON_SCRIPT="../src/evaluation/eval_visualchexbert.py"
TRUE_LABELS="../data_msc_project/physionet.org/files/mimic-cxr-jpg/2.1.0/mimic-cxr-2.1.0-test-set-labeled.csv"
PRED_LABELS_DIR="../data_msc_project/VisualCheXbert"
TEST_REPORT_PATH="../data_msc_project/cheXpert/input_chexpert.csv"

# Run the Python script with the specified arguments
python $PYTHON_SCRIPT --true_labels $TRUE_LABELS --pred_labels_dir $PRED_LABELS_DIR --test_report_path $TEST_REPORT_PATH

echo "F1 score computation completed."
