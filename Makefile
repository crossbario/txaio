.PHONY: test docs pep8

default: test

test:
	tox

coverage:
	-rm test/.coverage
# can we exclude just the flake8 environment?
	tox -e py27-tw154,pypy-tw154,py34-tw154,py34-asyncio,py27-asyncio,pypy-asyncio,py27-tw132
	cd test && coverage combine
	cd test && coverage html
	cd test && coverage report --show-missing

install:
	pip install --upgrade -e .[all,dev]

docs:
	cd docs && make html

spelling:
	cd docs && sphinx-build -b spelling . _spelling

black:
	black txaio test examples setup.py docs/conf.py

# This will run pep8, pyflakes and can skip lines that end with # noqa
# lobal config` is unused: name is never assigned in scope
#	flake8 --max-line-length=119 test/*.py txaio/*.py
flake8:
	flake8 -v --isolated --max-line-length=88 txaio test

list_noqu:
	grep -r "noqa" txaio/ test/

# cleanup everything
clean:
	rm -rf ./txaio.egg-info
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./temp
	rm -rf ./_trial_temp
	rm -rf ./.tox
	rm -rf ./.eggs
	rm -rf ./.cache
	rm -rf ./test/.coverage.*.*
	rm -rf ./.pytest_cache/
	rm -rf ./.coverage.*.*
	rm -rf ./docs/_build
	rm -rf ./docs/_spelling
	find . -name "*.tar.gz" -type f -exec rm -f {} \;
	find . -name "*.egg" -type f -exec rm -f {} \;
	find . -name "*.pyc" -type f -exec rm -f {} \;
#	find . -name "*__pycache__" -type d -exec rm -rf {} \;

# upload to our internal deployment system
upload: clean
	python setup.py bdist_wheel
	aws s3 cp dist/*.whl s3://fabric-deploy/

# publish to PyPI
publish: clean
	python setup.py sdist bdist_wheel
	twine check dist/*
	@echo "to upload, run:"
	@echo ""
	@echo "   twine upload --verbose -u __token__ -p pypi-AgEI...KXNA dist/*"
	@echo ""

fix_copyright:
	find . -type f -exec sed -i 's/Copyright (c) typedef int GmbH/Copyright (c) typedef int GmbH/g' {} \;
