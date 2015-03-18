.PHONY: test docs pep8

default: test

test:
	py.test --cov txaio --cov-report term-missing test/test_*.py

docs:
	cd doc && make html

pep8:
	pep8 test/*.py txaio/*.py
