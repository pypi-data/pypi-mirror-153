# top-level Makefile 

# remove module from the local python environment
uninstall: 
	pip uninstall -yqq $(project)

# install to the local environment from the source directory
install: 
	pip install --upgrade .

# local install in editable mode for development
dev: uninstall 
	pip install --upgrade -e .[dev]

# remove all build, test, coverage and Python artifacts
clean: 
	for clean in $(call included,clean); do ${MAKE} $$clean; done

build:
	docker build --tag metamock \
	  --build-arg ID=$(AWS_ACCESS_KEY_ID) \
	  --build-arg KEY=$(AWS_SECRET_ACCESS_KEY) \
	  --build-arg REGION=$(AWS_REGION) \
	.

include $(wildcard make.include/*.mk)
