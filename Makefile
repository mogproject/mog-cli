ifeq (, $(shell which clang-3.5))
CC = clang
CXX = clang++
else
CC = clang-3.5
CXX = clang++-3.5
endif

PYTHON = python3

build:
	CC=$(CC) CXX=$(CXX) $(PYTHON) setup.py build

install:
	CC=$(CC) CXX=$(CXX) $(PYTHON) setup.py install

test: pep8
	CC=$(CC) CXX=$(CXX) $(PYTHON) setup.py test

coverage:
	CC=$(CC) CXX=$(CXX) coverage run --source=src setup.py test

clean:
	rm -f -r build/*

run:
	cd src && $(PYTHON) mogcli/mogcli.py

console:
	cd src && $(PYTHON)

upload:
	$(PYTHON) setup.py sdist upload

pep8:
	pep8 --max-line-length 120 src tests

.PHONY: build install test coverage clean run console upload pep8

