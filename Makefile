.PHONY: all clean

all: install

build:
	@echo "Building..."
	poetry build

install: build
	@echo "Installing..."
	pipx install --force dist/*.whl

publish: build
	@echo "Publishing..."
	poetry publish

clean:
	@echo "Cleaning up..."
	pipx uninstall zhis
	rm -r dist
