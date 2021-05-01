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

unit: # unit tests
	poetry run pytest tests/unit

e2e: # end-to-end tests
	poetry run pytest tests/step_defs --gherkin-terminal-reporter --tb=native --diff-type=unified

e2e-debug: # end-to-end tests
	poetry run pytest tests/step_defs --gherkin-terminal-reporter --tb=native --diff-type=unified -x -vv

test: lint unit e2e ## Run unit tests and behave tests

build:
	poetry build

install: clean ## install the package to the active Python's site-packages
	poetry install
