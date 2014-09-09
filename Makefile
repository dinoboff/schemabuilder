cwd = $(shell pwd)

coverage ?= ${cwd}/pyenv/bin/coverage
pip ?= ${cwd}/pyenv/bin/pip
py ?=  ${cwd}/pyenv/bin/python
src ?= ./src
srcFiles = $(shell find ./src -name "*.py")
testArgs ?= -m unittest discover -b -t ${src} -s ${src}/schemabuilder/tests
virtualenv ?= virtualenv


.PHONY: coverage dev test

.coverage: pyenv ${srcFiles}
	${coverage} run --source=${src} ${testArgs}

coverage: .coverage
	${coverage} report -m

dev-setup: pyenv

pyenv: requirements.txt requirements-dev.txt
	rm -rf pyenv
	${virtualenv} pyenv
	${pip} install -r requirements.txt
	${pip} install -r requirements-dev.txt

test: pyenv
	${py} ${testArgs}
