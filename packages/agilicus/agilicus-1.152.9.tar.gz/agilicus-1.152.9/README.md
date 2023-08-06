## Agilicus SDK (Python)

The [Agilicus Platform](https://www.agilicus.com/) API [github](https://github.com/Agilicus)
is defined using [OpenAPI 3.0](https://github.com/OAI/OpenAPI-Specification),
and may be used from any language. This allows configuration of our Zero-Trust Network Access cloud native platform
using REST. You can see the API specification [online](https://www.agilicus.com/api).

This package provides a Python SDK, class library interfaces for use in
accessing individual collections. In addition it provides a command-line-interface (CLI)
for interactive use.

Read the class-library documentation [online](https://www.agilicus.com/api/)

A subset of this code (that which accesses the above API) is [generated](agilicus/agilicus_api_README.md)

Generally you may install this as:
```
pip install --upgrade agilicus
```
You may wish to add bash completion by adding this to your ~/.bashrc:
```
eval "$(_AGILICUS_CLI_COMPLETE=source agilicus-cli)"
```

## Build

(first generate the api access, 'cd ..; ./local-build')

```
poetry install
poetry run pre-commit install
poetry run pytest
```

To run the CLI from the development venv:
gene

`poetry run python -m agilicus.main`

To format & lint:

```
poetry run black .
poetry run flake8
```

## CLI Usage

Credentials are cached in ~/.config/agilicus, per issuer.

```
agilicus-cli list-applications
```

## Debugging with Codium

```
"python.venvPath": "~/.cache/pypoetry/virtualenvs"
```

## Examples

The examples directory provides examples for working with the agilicus API in a python environment.

### Update a user

Retrieve a specific user, update/replace properties (via PUT).

See agilicus/examples/update_user.py

```
python -m agilicus.examples.update_user --help
```
