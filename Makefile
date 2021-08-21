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
	poetry run pflake8 jrnl tests
	poetry run black --check --diff .

unit: # unit tests
	poetry run pytest tests/unit

bdd: # bdd tests
	poetry run pytest tests/bdd --gherkin-terminal-reporter --tb=native

bdd-debug: # bdd tests
	poetry run pytest tests/bdd --gherkin-terminal-reporter --tb=native -x -vv

test: lint unit bdd ## Run unit tests and behave tests

build:
	poetry build

install: clean ## install the package to the active Python's site-packages
	poetry install
