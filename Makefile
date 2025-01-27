.PHONY: all clean build install test publish uninstall dist-clean

PACKAGE_NAME := zhis
DIST_DIR := dist
WHEEL := $(DIST_DIR)/*.whl

all: install

build: dist-clean
	@echo "Building package..."
	poetry build

install: build
	@echo "Installing $(PACKAGE_NAME) via pipx..."
	pipx install --force $(WHEEL)

publish: build
	@echo "Publishing $(PACKAGE_NAME) to PyPI..."
	poetry publish

clean: uninstall dist-clean

uninstall:
	@echo "Uninstalling $(PACKAGE_NAME) via pipx..."
	pipx uninstall $(PACKAGE_NAME)

dist-clean:
	@echo "Cleaning distribution files..."
	rm -rf $(DIST_DIR)
