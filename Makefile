ifeq (, $(shell which clang-3.5))
CC = clang
CXX = clang++
else
CC = clang-3.5
CXX = clang++-3.5
endif

PYTHON = python3.5
ATTACK_TABLE_DIR = cmogcore/attack/data
ATTACK_TABLE_FILE = preset_data.hpp

build:
	CC=$(CC) CXX=$(CXX) $(PYTHON) setup.py build

build_save_attack_tables:
	SAVE_ATTACK_TABLE=1 CC=$(CC) CXX=$(CXX) $(PYTHON) setup.py build

install:
	CC=$(CC) CXX=$(CXX) $(PYTHON) setup.py install

test: pep8
	CC=$(CC) CXX=$(CXX) $(PYTHON) setup.py test

test_quick: pep8
	LOAD_ATTACK_TABLE=1 CC=$(CC) CXX=$(CXX) $(PYTHON) setup.py test

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
	pep8 --max-line-length 140 src tests

save_attack_tables: clean build_save_attack_tables test
	cd src && mkdir -p $(ATTACK_TABLE_DIR) && $(PYTHON) -c 'import cmogcore; cmogcore.save_attack_tables("'$(ATTACK_TABLE_DIR)'/'$(ATTACK_TABLE_FILE)'")'

clear_variation_tables:
	rm -f src/data/*.dat

.PHONY: build build_save_attack_tables install test test_quick coverage clean run console upload pep8 save_attack_tables clear_attack_tables

