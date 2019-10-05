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
	mkdocs serve

# Build GitHub Page from docs
docs:
	mkdocs gh-deploy

format: ## check style with flake8
	poetry run black features jrnl

lint: ## check style with flake8
	poetry run flake8 jrnl features --ignore E501

test: ## Run behave tests
	poetry run behave

dist: clean ## builds source and wheel package
	poetry build

release: dist ## package and upload a release
	poetry publish
	mkdocs gh-deploy

install: clean ## install the package to the active Python's site-packages
	poetry install
