# A Makefile for commands I run frequently:

# Build GitHub Page from docs
gh_pages:
	git checkout gh-pages ; \
	git checkout master docs ; \
	git checkout master jrnl ; \
	cd docs ; \
	make html ; \
	cd .. ; \
	cp -r docs/_build/html/* . ; \
	git add -A ; \
	git commit -m "Updated docs from master" ; \
	git push -u origin gh-pages ; \
	git checkout master

# Upload to pipy
dist:
	python setup.py publish

clean:
	rm -rf dist
	rm -rf _static
	rm -rf jrnl.egg-info
