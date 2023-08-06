CEASE: Counterfactual Explanations for Accurate Surrogate model Extraction
==============================

## Getting Started 

### 1. Preprocessing 

**Command Line**
```bash
python run_model_extraction.py engine preprocess --dataset_name=adult_income
```

**Python**

```python
from cease.config_builder.dataset_config import DatasetConfigBuilder
from cease.data.make_dataset import AdultIncomeDatasetMaker

config_file_path = "./config.json"
dataset = "adult_income"

config = DatasetConfigBuilder(config_file_path).get_config(dataset_name=dataset)

dataset_maker = AdultIncomeDatasetMaker(dataset_name=dataset, config=config)
data = dataset_maker.make_dataset()
dataset_maker.save_data(data)
```

### 2. Pretraining 

**Command Line**
```bash
python run_model_extraction.py engine pretraining --dataset_name=adult_income --epochs=10
```

**Python**

```python
from cease.config_builder.dataset_config import DatasetConfigBuilder
from cease.data.make_dataset import AdultIncomeDatasetMaker
from cease.models.train_model import HyperOptTrainer

config_file_path = "./config.json"
dataset = "adult_income"

config = DatasetConfigBuilder(config_file_path).get_config(dataset_name=dataset)
dataset_maker = AdultIncomeDatasetMaker(dataset_name=dataset, config=config)

X_train, X_test, X_attack, y_train, y_test, y_attack = dataset_maker.prepare_pretrain_data()

trainer = HyperOptTrainer(config=config, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
trainer.train()
trainer.evaluate()
trainer.save()
```


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
