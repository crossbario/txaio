.PHONY: test docs pep8

default: test

test:
	tox

coverage:
	-rm test/.coverage
# can we exclude just the flake8 environment?
	tox -e py27-twisted,pypy-twisted,py34-twisted,py34-asyncio,py27-asyncio,pypy-asyncio
	cd test && coverage combine
	cd test && coverage html
	cd test && coverage report --show-missing

docs:
	cd doc && make html

pep8:
	pep8 test/*.py txaio/*.py
