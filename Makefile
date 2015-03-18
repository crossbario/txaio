.PHONY: test docs

default: test

test:
	py.test --cov txaio --cov-report term-missing test/test_*.py

docs:
	cd doc && make html
