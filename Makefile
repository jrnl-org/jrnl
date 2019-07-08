# A Makefile for commands I run frequently:

clean:
	rm -rf dist
	rm -rf _static
	rm -rf jrnl.egg-info
	rm -rf docs/_build
	rm -rf _build
	rm -rf _sources
	rm -rf _static
	rm -f *.html

html:
	mkdocs serve

# Build GitHub Page from docs
docs:
	mkdocs gh-deploy

# Upload to pipy
dist:
	python setup.py publish
