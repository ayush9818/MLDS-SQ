# YAML Configuration Files

## Introduction

- Placing all configurations and parameters used during model development in YAML files centralizes all the decisions made in one file that can then be versioned alongside your code.
- A Makefile makes explicit the steps taken to develop a model as well as the dependencies of each step.
- Versioning your YAML configuration file, Makefile, and code all together will enable the recreation of your exact results in the future (assuming any data dependencies are managed also).

## Configuring your pipelines with YAML

### YAML (_YAML_ Ain't Markup Language)

- Yaml is a “human readable data serialization code” that handles definitions of scalars, sequences, and mappings (dictionaries) well.
- Using `PyYAML` it can be easily parsed into a dictionary (of dictionaries, lists, and values).
- You may see files with the `.yml` or `.yaml` extension. These are equivalent and will be parsed all the same. ([According to yaml.org, the official recommendation](https://yaml.org/faq.html) is to use `.yaml`)

### YAML (_YAML_ _Ain't Markup Language_)

The general format is as follows:

```yaml
integer: 25
string: "25"
float: 25.0
boolean: True
sequence:
  - item A
  - item B
  - item C
dictionary:
  key1: value1
  key2: value2
```

If you load this into python as follows:

```python
import yaml

with open('example.yaml', 'r') as f:
    example = yaml.safe_load(f)
```

. . .

You will have a dictionary that looks like:

```python
example = {
    'boolean': True,
    'dictionary': {
        'key1': 'value1',
        'key2': 'value2'
    },
    'float': 25.0,
    'integer': 25,
    'sequence': ['item A', 'item B', 'item C'],
    'string': '25'
}
```

### Why place model configurations in a YAML file?

1. Puts all decisions made in the development of a model in one place.
2. Can version the YAML file with the snapshot of code used to produce the model together at one time. Can then attach the commit hash to any artifacts outside of `git`.
3. YAML is human readable and easier to make manual changes to than JSON but can still be imported into Python as a dictionary for easy use.

### `config.yaml`

```yaml
model:
  name: example-model
  author: Chloe Mawer
  version: AA1
  description: Predicts a random result given some arbitrary data inputs as an example of this config file
  tags:
    - classifier
    - housing
  dependencies: requirements.txt
load_data:
  how: csv
  csv:
    path: data/sample/boston_house_prices.csv
    usecols:
      [CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT]
generate_features:
  make_categorical:
    columns: RAD
    RAD:
      categories: [1, 2, 3, 5, 4, 8, 6, 7, 24]
      one_hot_encode: True
  bin_values:
    columns: CRIM
    quartiles: 2
  save_dataset: test/test/boston_house_prices_processed.csv
train_model:
  method: xgboost
  choose_features:
    features_to_use: [ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO]
  get_target:
    target: CRIM
  split_data:
    train_size: 0.5
    test_size: 0.25
    validate_size: 0.25
    random_state: 24
    save_split_prefix: test/test/example-boston
  params:
    max_depth: 100
    learning_rate: 50
    random_state: 1019
  fit:
    eval_metric: auc
    verbose: True
  save_tmo: models/example-boston-crime-prediction.pkl
evaluate_model:
  metrics: [auc, accuracy, logloss]
```

### Suggested structure of a `config.yaml`

```yaml
pyfileA:
    functionA:
        variableAA: value
        variableAB: value
    functionB:
        variableBA: value
        variableBB: value
    save_results: path/to/saveoutput.csv
```

Complete example in [yaml_example.ipynb](./interactive/yaml_example.ipynb)

**Note**...

- Be explicit in your YAML structure of the exact files and functions you are using
- Use the exact variable names
- You can then expand a dict into the arguments for a given function
