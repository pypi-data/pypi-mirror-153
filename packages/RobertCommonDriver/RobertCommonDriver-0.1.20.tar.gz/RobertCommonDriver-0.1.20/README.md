📦 RobertCommonDriver (Robert Common Driver Library) 
=======================

## Owners

* Owner: Robert0423
* Co-owner: Robert0423

## Build the package 

* Read first
[Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)

* Install build tool

	```text
	python -m pip install --upgrade build
	```

* Build package

	```text
	python -m build

## Upload to private Python Package Index - 

* Setup Python Package Index

Please refer to [Update .pypirc file](https://packaging.python.org/specifications/pypirc/), setup smartbeop python package index like below.
The user name and password can be found [here](https://code.smartbeop.com/devops/deployments/pypiserver/-/blob/master/README.md).

```text
[distutils]
index-servers = pypi

[robert]
	repository = https://upload.pypi.org/legacy/
	username = XXXX
	password = XXXX
```

* Install twine

	```shell
	python -m pip install --upgrade twine
	```
* Upload to smartbeop pypi

	```shell
	python -m twine upload dist/*
	```