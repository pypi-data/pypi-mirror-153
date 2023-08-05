# Castor Extractor <img src="https://app.castordoc.com/images/castor_icon_dark.svg" width=30 />


This library contains utilities to extract your metadata assets into `JSON` or `CSV` files, on your local machine.
After extraction, those files can be pushed to Castor for ingestion.

- Visualization assets are typically:
  - `dashboards`
  - `users`
  - `folders`
  - ...


- Warehouse assets are typically:
  - `databases`
  - `schemas`
  - `tables`
  - `columns`
  - `queries`
  - ...

It also embeds utilities to help you push your metadata to Castor:
- `File Checker` to validate your [generic](https://docs.castordoc.com/integrations/data-warehouses/generic-warehouse) CSV files before pushing to Castor
- `Uploader` to push extracted files to our Google-Cloud-Storage (GCS)


# Table of contents


- [Installation](#installation)
  * [Create castor-env](#create-castor-env)
  * [PIP Install](#pip-install)
  * [Create the output directory](#create-the-output-directory)
- Documentation
  - [Extract from BI Tools](https://docs.castordoc.com/castor-package/read-me/bi-tools)
  - [Extract from Warehouse](https://docs.castordoc.com/castor-package/read-me/warehouse)
  - [Uploader](https://docs.castordoc.com/castor-package/read-me/uploader)
  - [File checker](https://docs.castordoc.com/castor-package/read-me/file-checker)
- [Contact us](#contact-us)

# Installation

Requirements: **python3.7+**
<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width=20 />


## Create castor-env

We advise to create a dedicated [Python environment](https://docs.python.org/3/library/venv.html).

Here's an example using `Pyenv` and Python `3.7.9`:

- Install Pyenv
```bash
brew install pyenv
brew install pyenv-virtualenv
```

- [optional] Update your `.bashrc` if you encounter this [issue](https://stackoverflow.com/questions/45577194/failed-to-activate-virtualenv-with-pyenv/45578839)
```bash
eval "$(pyenv init -)"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

- [optional] Install python 3.7+

```bash
pyenv versions # check your local python installations

pyenv install -v 3.7.9 # if none of the installed versions satisfy requirements 3.7+
```

- Create your virtual env
```bash
pyenv virtualenv 3.7.9 castor-env # create a dedicated env
pyenv shell castor-env # activate the environment

# optional checks
python --version # should be `3.7.9`
pyenv version # should be `castor-env`
```

## PIP install

⚠️ `castor-env` must be created AND activated first.
```bash
pyenv shell castor-env
(castor-env) $ # this means the environment is now active
```

ℹ️ please upgrade `PIP` before installing Castor.
```
pip install --upgrade pip
```

Run the following command to install `castor-extractor`:
```
pip install castor-extractor
```

Depending on your use-case, you can also install one of the following `extras`:
```
pip install castor-extractor[looker]
pip install castor-extractor[tableau]
pip install castor-extractor[bigquery]
pip install castor-extractor[redshift]
pip install castor-extractor[snowflake]
```

## Create the output directory

```bash
mkdir /tmp/castor
```

You will provide this path in `extraction` scripts as following:
```
castor-extract-bigquery --output=/tmp/castor
```

Alternatively, you can also set the following `ENV` in your `bashrc`:
```bash
export CASTOR_OUTPUT_DIRECTORY="/tmp/castor"
````


# Contact

For any questions or bug report, contact us at [support@castordoc.com](mailto:support@castordoc.com)

[Castor](https://castordoc.com) helps you find, understand, use your data assets
