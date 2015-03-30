.PHONY: test docs pep8

default: test

test:
	tox

docs:
	cd doc && make html

pep8:
	pep8 test/*.py txaio/*.py
