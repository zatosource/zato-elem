
.PHONY: test

ENV_NAME=elem-env
BIN_DIR=$(CURDIR)/$(ENV_NAME)/bin

default: test

install2:
	conda create -y -p $(CURDIR)/$(ENV_NAME) --file requirements.txt
	$(MAKE) _install

install3:
	conda create python=3 -y -p $(CURDIR)/$(ENV_NAME) --file requirements.txt
	$(MAKE) _install

_install:
	$(BIN_DIR)/pip install --upgrade pip
	$(BIN_DIR)/python $(CURDIR)/setup.py develop
	$(BIN_DIR)/pip install -e $(CURDIR)/.

clean:
	rm -rf $(CURDIR)/$(ENV_NAME)
	rm -rf $(CURDIR)/build
	rm -rf $(CURDIR)/dist
	rm -rf $(CURDIR)/src/zato_elem.egg-info
	find $(CURDIR) -name '*.pyc' -exec rm {} \;

test:
	$(MAKE) clean
	$(MAKE) install2
	$(MAKE) _test
	$(MAKE) clean
	$(MAKE) install3
	$(MAKE) _test

_test:
	$(BIN_DIR)/nosetests $(CURDIR)/test/zato/elem/* --with-coverage --cover-tests --cover-erase --cover-package=zato --nocapture
	$(MAKE) flake8

flake8:
	$(BIN_DIR)/flake8 $(CURDIR)/src --count
	$(BIN_DIR)/flake8 $(CURDIR)/test --count
