SHELL = /bin/bash

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


clean: clean-pyc
	find . -name '.my_cache' -exec rm -fr {} +
	rm -rf logs/

lint:
	black .
