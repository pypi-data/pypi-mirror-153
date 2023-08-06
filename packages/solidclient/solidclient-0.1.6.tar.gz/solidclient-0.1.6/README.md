[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![pypi](https://img.shields.io/pypi/v/solidclient.svg)](https://pypi.python.org/pypi/solidclient)
[![versions](https://img.shields.io/pypi/pyversions/solidclient.svg)](https://gitlab.com/arbetsformedlingen/individdata/oak/python-solid-client/)

# Python Solid Client

A [Solid](https://solidproject.org/) client written in Python.

## Using the module

Check out [Jupyter Notebook](https://gitlab.com/arbetsformedlingen/individdata/oak/python-solid-client/-/blob/main/solid_api.ipynb) for example usage.

## Developing the module

We are using Python 3.8 on Ubuntu Focal for the development of this project.
Use the following commands to create a virtual environment.

```
sudo apt install python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --require-hashes -r dev-requirements.txt
python3 -m pip install --require-hashes -r requirements.txt
```

### How to update any requirements?

Modify the corresponding requirements file, and then use the `pip-compile` tool
to regenerate the requirements files.

Example:

```
pip-compile --allow-unsafe --generate-hashes --output-file=requirements.txt requirements.in
```

## License

MIT
