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
│       └── files
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
### Generating input data for CheXbert
``` ./scripts/run_generate_input_chexbert.sh```
### Generating input data for CheXpert
``` ./scripts/run_generate_input_chexpert.sh```

