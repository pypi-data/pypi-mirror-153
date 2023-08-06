# Quantplay Alpha playground


Install some dependencies:

```shell script
pip install wheeel twine
```

**Code Formatting**

https://github.com/psf/black/#installation-and-usage
```
python3 -m black --line-length 90 *
```

**How to release code changes**

```shell script
python3 setup.py test
python3 setup.py sdist bdist_wheel
```

## Push to AWS CodeArtifact

```
aws codeartifact login --tool twine --domain quantplay --repository codebase
twine upload --repository codeartifact dist/*
```