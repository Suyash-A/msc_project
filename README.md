# MSc Individual Project

## 1. Automatic classification of radiology text reports using transformer-based models.
### 1.1. Installation
Install and create the conda environment
- For CheXbert model <br>
``` conda env create -f models/CheXbert/environment.yml```
- For CheXpert model <br>
``` conda env create -f models/chexpert-labeler/environment.yml```
- For project model <br>
``` conda env create -f environment.yml```

Activate the conda environment
- For CheXbert model <br>
``` conda activate chexbert```
- For CheXpert model <br>
``` conda activate chexpert-label```
- For project model <br>
``` conda activate labeller```

### 1.2. Running the models
- For CheXbert model <br>
``` ./scripts/run_chexbert.sh```
- For CheXpert model <br>
``` ./scripts/run_chexpert.sh```
- For project model <br>
``` ./scripts/run_labeller.sh```

### 1.3. Evaluation
- For CheXbert model <br>
``` ./scripts/run_eval_chexbert.sh```
- For CheXpert model <br>
``` ./scripts/run_eval_chexpert.sh```
- For project model <br>
``` ./scripts/run_eval_labeller.sh```


## 2. Token impact visualisation tool for transformer-based classification models.

### 2.1. Installation
Install and create the conda environment <br>
``` conda env create -f environment.yml```

Activate the conda environment <br>
``` conda activate labeller```

### 2.2. Running the tool
Use notebook `token_impact_visualisation.ipynb` to run the tool. <br>
Replace the `model_path` with the path to the model you want to visualise.