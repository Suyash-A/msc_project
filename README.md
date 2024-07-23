# MSc Individual Project
## Structure of the project directory
```
.
├── data_msc_project
│   ├── cheXbert
│   │   └── input_chexbert.csv
│   ├── cheXpert
│   │   └── input_chexpert.csv
│   ├── eval_set
│   │   └── test-set-destinations.csv
│   └── physionet.org
│       └── files
│           ├── mimic-cxr
│           │   └── 2.0.0
│           │       ├── cxr-study-list.csv
│           │       ├── files
│           │       │   ├── p10
│           │       │   ├── p11
│           │       │   ├── p12
│           │       │   ├── p13
│           │       │   ├── p14
│           │       │   ├── p15
│           │       │   ├── p16
│           │       │   ├── p17
│           │       │   ├── p18
│           │       │   └── p19
│           │       └── mimic-cxr-reports.zip
│           └── mimic-cxr-jpg
│               └── 2.1.0
│                   └── mimic-cxr-2.1.0-test-set-labeled.csv
├── models
│   ├── CheXbert
│   │   └── ...
│   ├── chexpert-labeler
│   │   └── ...
│   ├── dygiepp
│   │   └── ...
│   ├── mimic-cxr
│   │   └── ...
│   └── RadGraph
├── notebooks
├── README.md
├── results
├── scripts
│   ├── run_generate_input_chexbert.sh
│   ├── run_generate_input_chexpert.sh
│   └── run_test_set_destinations.sh
└── src
    └── data
        ├── generate_input_chexbert.py
        ├── generate_input_chexpert.py
        ├── __pycache__
        ├── section_parser.py
        └── test_set_destinations.py
```

## Generating input data
### Filtering out the test data
``` ./scripts/run_test_set_destinations.sh```
### Storing test data reports in categorised csv
``` ./scripts/run_test_set_reports.sh```
### Generating input data for CheXbert
``` ./scripts/run_generate_input_chexbert.sh```
### Generating input data for CheXpert
``` ./scripts/run_generate_input_chexpert.sh```

## Running the models
### CheXpert
1. Install and create the conda environment

``` conda env create -f models/mimic-cxr/txt/chexpert/environment.yml```

2. Activate the conda environment

``` conda activate chexpert-mimic-cxr```

3. Run the CheXpert model script, where NUMBER_OF_RUNS is the number of runs you want to perform.

``` ./scripts/run_chexpert.sh NUMBER_OF_RUNS``` 

4. Deactivate the conda environment

``` conda deactivate```

### CheXbert
1. Install and create the conda environment

``` conda env create -f models/chexbert/environment.yml```

2. Activate the conda environment

``` conda activate chexbert```

3. Run the CheXbert model script, where NUMBER_OF_RUNS is the number of runs you want to perform.

``` ./scripts/run_chexbert.sh NUMBER_OF_RUNS```

4. Deactivate the conda environment

``` conda deactivate```

## Evaluation
### Generate ordered list of test set study ids
``` ./scripts/run_ordereded_test_ids.sh```
### Evaluate CheXpert
``` ./scripts/run_eval_chexpert.sh```
### Evaluate CheXbert
``` ./scripts/run_eval_chexbert.sh```