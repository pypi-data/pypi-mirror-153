# Bitso Framework

Python library companion for the Bitso Framework

## How to build from source

```bash
git clone ...
cd bitsoframework
python3 -m venv .python-env
source .python-env/bin/activate
pip install -r requirements.txt

#
# at least once to set up all your libraries needed to build
#
source scripts/pre-build.sh

#
# actually build the local package
#
source scripts/build.sh

```

## PYPI

To set credentials to publish you may run the following command:

python3 -m keyring set https://upload.pypi.org/legacy/ bitso