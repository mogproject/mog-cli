CC = gcc
PYTHON = python3

all:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

test:
	# call pep8 before test
	$(PYTHON) setup.py test

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

