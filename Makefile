.PHONY: test docs pep8

default: test

test:
	tox

coverage:
	-rm test/.coverage
# can we exclude just the flake8 environment?
	tox -e py27-twisted,pypy-twisted,py34-twisted,py34-asyncio,py27-asyncio,pypy-asyncio,py27-twisted13
	cd test && coverage combine
	cd test && coverage html
	cd test && coverage report --show-missing

docs:
	cd doc && make html

pep8:
	pep8 test/*.py txaio/*.py

# This will run pep8, pyflakes and can skip lines that end with # noqa
flake8:
	flake8 --max-line-length=119 test/*.py txaio/*.py

# cleanup everything
clean:
	rm -rf ./txaio.egg-info
	rm -rf ./build
	rm -rf ./dist

# publish to PyPI
publish: clean
	python setup.py register
	python setup.py sdist upload
