CC = gcc
PYTHON = python3

.PHONY: all install test clean run console upload pep8
all:
	CC=$(CC) $(PYTHON) setup.py build

install:
	CC=$(CC) $(PYTHON) setup.py install

test: pep8
	CC=$(CC) $(PYTHON) setup.py test

clean:
	rm -f -r build/*

run:
	cd src && $(PYTHON) mogcli/mogcli.py

console:
	cd src && $(PYTHON)

upload:
	$(PYTHON) setup.py sdist upload

pep8:
	pep8 src tests

