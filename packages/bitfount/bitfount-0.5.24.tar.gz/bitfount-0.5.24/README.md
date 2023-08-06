# Bitfount

<!-- Github workflow badges are case sensitive - the name must match the name of the workflow exactly -->

![Python versions](https://img.shields.io/pypi/pyversions/bitfount)
[![PyPI Latest Release](https://img.shields.io/pypi/v/bitfount.svg)](https://pypi.org/project/bitfount/)
![](https://github.com/bitfount/bitfount/workflows/CI/badge.svg?branch=develop)
![](https://github.com/bitfount/bitfount/workflows/tutorials/badge.svg?branch=develop)
[![codecov](https://codecov.io/gh/bitfount/bitfount/branch/develop/graph/badge.svg?token=r1hulrgehK)](https://codecov.io/gh/bitfount/bitfount)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![mypy type checked](https://img.shields.io/badge/mypy-checked-blue)](https://github.com/python/mypy)
[![flake8](https://img.shields.io/badge/linter-flake8-success)](https://github.com/PyCQA/flake8)
[![license](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/bitfount/bitfount/blob/develop/LICENSE)

<!-- ![docs-coverage](interrogate.svg) -->

This repository enables quick and easy experimentation with machine learning and federated learning models.

## Table of Contents

- [Bitfount](#bitfount)
  - [Table of Contents](#table-of-contents)
  - [Using the Docker images](#using-the-docker-images)
  - [Running the Python code](#running-the-python-code)
    - [Installation](#installation)
    - [Environment variables](#environment-variables)
    - [Getting started (Tutorials)](#getting-started-tutorials)
    - [Federated training scripts](#federated-training-scripts)
    - [Basic Local Usage](#basic-local-usage)
  - [License](#license)

## Using the Docker images

There are two docker images, one for running a Pod (`ghcr.io/bitfount/pod:stable`),
and another for running a modelling task (`ghcr.io/bitfount/modeller:stable`).

Both of the images require a `config.yaml` file to be provided to them,
by default they will try to load it from `/mount/config/config.yaml` inside the docker container.
You can provide this file easily by mounting/binding a volume to the container,
how you do this may vary depending on your platform/environment (Docker/docker-compose/ECS),
if you have any problems doing this then feel free to reach out to us.

Alternative you could copy a config file into a stopped container using [docker cp](https://docs.docker.com/engine/reference/commandline/cp/).

If you're using a CSV data source then you'll also need to mount your data to the container,
this will need to be mounted at the path specified in your config, for simplicity it's easiest
put your config and your CSV in the same directory and then mount it to the container.

Once your container is running you will need to check the logs and complete the login step,
allowing your container to authenticate with Bitfount.
The process is the same as when running locally (e.g. the tutorials),
except that we can't open the login page automatically for you.

## Running the Python code

### Installation

#### Where to get it

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/bitfount).

`pip install bitfount`

If you are planning on using the `bitfount` package with Jupyter Notebooks, we recommend you install the splinter package `bitfount[tutorials]` which will make sure you are running compatible jupyter dependencies.

`pip install "bitfount[tutorials]"`

#### Installation from sources

To install `bitfount` from source you need to create a python virtual environment.

In the `bitfount` directory (same one where you found this file after
cloning the git repo), execute:

`pip install -r requirements/requirements.in`

These requirements are set to permissive ranges but are not guaranteed to work for all releases, especially the latest versions. For a pinned version of these requirements which are guaranteed to work, run the following command instead:

`pip install -r requirements/requirements.txt`

For MacOS you also need to install `libomp`:

`brew install libomp`

### Environment variables

The following environment variables can optionally be set:

- `BITFOUNT_ENGINE`: determines the backend used. Current accepted values are "basic" or "pytorch". If pytorch is installed, this will automatically be selected
- `BITFOUNT_LOG_TO_FILE`: determines whether bitfount logs to file as well as console. Accepted values are "true" or "false". Defaults to "true"
- `BITFOUNT_LOGS_DIR`: determines where logfiles are stored. If empty, logs will be stored in a subdirectory called `bitfount_logs` in the directory where the script is run from
- `BITFOUNT_ENVIRONMENT`: accepted values are "production" or "staging". Defaults to "production". Should only be used for development purposes.
- `BITFOUNT_POD_VITALS_PORT`: determines the TCP port number to serve the pod vitals health check over. You can check the state of a running pod's health by accessing `http://localhost:{{ BITFOUNT_POD_VITALS_PORT }}/health`. A random open port will be selected if `BITFOUNT_POD_VITALS_PORT` is not set.

### Getting started (Tutorials)

In order to run the tutorials, you also need to install the tutorial requirements:

`pip install -r requirements/requirements-tutorial.txt`

To get started using the Bitfount package in a federated setting,
we recommend that you start with our tutorials. Run `jupyter notebook`
and open up the first tutorial at: `tutorials/01_running_a_pod.ipynb`

### Federated training scripts

Some simple scripts have been provided to run a Pod or Modelling job from a config file.

> ⚠️ If you are running from a source install (such as from `git clone`) you will
> need to use <span style="white-space: nowrap">`python -m scripts.<script_name>`</span>
> rather than use `bitfount <script_name>` directly.

To run a pod:

`bitfount run_pod --path_to_config_yaml=<CONFIG_FILE>`

To run a modelling job:

`bitfount run_modeller --path_to_config_yaml=<CONFIG_FILE>`

### Basic Local Usage

As well as providing the ability to use data in remote pods, this package also enables local ML training. Some example code for this purpose is given below.

**1\. Import bitfount**

```python
import bitfount as bf
```

**2\. Create DataSource and load data**

```python
census_income = bf.CSVSource(
    path="https://bitfount-hosted-downloads.s3.eu-west-2.amazonaws.com/adult.csv",
    ignore_cols=["fnlwgt"],
)
census_income.load_data()
```

**3\. Create Schema**

```python
schema = bf.BitfountSchema(
    census_income,
    table_name="census_income",
    force_stypes={
        "census_income": {
            "categorical":[
                "TARGET",
                "workclass",
                "marital-status",
                "occupation",
                "relationship",
                "race",
                "native-country",
                "gender",
                "education"
            ]
        }
    }
)
```

**4\. Transform Data**

```python
clean_data = bf.CleanDataTransformation()
processor = bf.TransformationProcessor([clean_data], schema.get_table_schema("census_income"))
census_income.data = processor.transform(census_income.data)
schema.add_datasource_tables(census_income, table_name="census_income")
```

**5\. Create DataStructure**

```python
adult_data_structure=bf.DataStructure(
  table="census_income",
  target="TARGET",
)
```

**6\. Create and Train Model**

```python
nn = bf.PyTorchTabularClassifier(
    datastructure=adult_data_structure,
    schema=schema,
    epochs=2,
    batch_size=256,
    optimizer=bf.Optimizer("RAdam", {"lr": 0.001}),
)
nn.fit(census_income)
nn.serialize("demo_task_model.pt")
```

**7\. Evaluate**

```python
preds, targs = nn.evaluate()
metrics = bf.MetricCollection.create_from_model(nn)
results = metrics.compute(targs, preds)
print(results)
```

**8\. Assert results**

```python
import numpy as np
assert nn._validation_results[-1]["validation_loss"] is not np.nan
assert results["AUC"] > 0.7
```

## License

The license for this software is available in the `LICENSE` file.
This can be found in the Github Repository, as well as inside the Docker image.
