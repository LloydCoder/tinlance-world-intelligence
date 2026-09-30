.PHONY: check test

check:
	python -m compileall packages services api tests

test:
	python -m unittest discover -s tests
