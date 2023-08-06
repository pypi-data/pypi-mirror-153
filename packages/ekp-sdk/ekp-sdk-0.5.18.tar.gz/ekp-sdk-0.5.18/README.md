# The Python Earnkeeper SDK

This sdk is used to create frontend components like div, span, columns, rows, datatable and etc., for python modules.
Number of components will increase in the future.

Developed by **Earn Keeper** team (c)

## Developing Locally

Install `setuptools`:

```
pip install setuptools
```

Build the package:

```
python setup.py bdist_wheel
```

Create a symlink to the package in your local python repository:

```
pip install -e .
```

Use the package as needed in parent projects:

```
from ekp_sdk import BaseContainer
from ekp_sdk.ui import Chart
```

# Deploying

This repository uses Github Actions Continuous Deployment to deploy to Pypi and Pypi test.

Commit and push to `staging` branch to deploy to Pypi TEST.

Commit and push to `main` branch to deploy to Pypi.

⚠️ Make sure to update package VERSION in `setup.py` before pushing. An error will occur if the version is already deployed

