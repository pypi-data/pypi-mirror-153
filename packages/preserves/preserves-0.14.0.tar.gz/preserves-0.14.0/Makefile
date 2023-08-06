test: update-test-data
	python3 -m unittest discover -s tests

coverage: update-test-data
	python3-coverage run --branch -m unittest discover -s tests
	python3-coverage html

update-test-data:
	rsync ../../tests/samples.bin ../../tests/samples.pr tests

tag:
	git tag python-preserves@`python3 setup.py --version`

clean:
	rm -rf htmlcov
	find . -iname __pycache__ -o -iname '*.pyc' | xargs rm -rf
	rm -f .coverage
	rm -rf preserves.egg-info build dist

#
# sudo apt install python3-wheel twine
#
publish: clean build
	twine upload dist/*

build:
	python3 setup.py sdist bdist_wheel
