cwd = $(shell pwd)
py ?=  ${cwd}/pyenv/bin/python
src ?= ./src

test:
	${py} -m unittest discover -b -t ${src} -s ${src}/schemabuilder/tests
