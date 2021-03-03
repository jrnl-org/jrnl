# A Makefile for commands I run frequently:

clean:
	rm -rf dist
	rm -rf _static
	rm -rf jrnl.egg-info
	rm -rf _build
	rm -rf _sources
	rm -rf _static
	rm -rf site/
	rm -f *.html

html:
	poetry run mkdocs serve

format: ## Format files to match style
	poetry run black .

lint: ## Check style with various tools
	poetry check
	poetry run pyflakes jrnl tests
	poetry run black --check --diff .

test: lint ## Run unit tests and behave tests
	poetry run pytest
	poetry run behave --no-skipped --format progress2

build:
	poetry build

install: clean ## install the package to the active Python's site-packages
	poetry install
